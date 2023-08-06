import json
import urllib.parse
import datetime
import jwt

import requests
import agilicus
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import update_if_present

from . import context, response, token_parser

from .output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
)


def _create_token(
    ctx, user_id, duration, aud, hosts=[], roles={}, org_id=None, scopes=None
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Content-type"] = "application/json"

    data = {}
    data["sub"] = user_id
    data["time_validity"] = {"duration": duration}
    data["audiences"] = aud
    if hosts:
        data["hosts"] = hosts
    if org_id:
        data["org"] = org_id
    if roles:
        data["roles"] = roles
    if scopes:
        data["scopes"] = scopes

    response = requests.post(
        context.get_api(ctx) + "/v1/tokens",
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    return response


def get_introspect(ctx, raw_token, exclude_roles, *, show_suborgs, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    options = agilicus.TokenIntrospectOptions(exclude_roles=exclude_roles)
    token_obj = agilicus.TokenIntrospect(token=raw_token, introspect_options=options)

    if not show_suborgs:
        resp = apiclient.tokens_api.create_introspect_token(token_obj, **kwargs)
    else:
        resp = apiclient.tokens_api.create_introspect_token_all_sub_orgs(
            token_obj, **kwargs
        )

    return resp


def get_token(ctx, user_id, org_id, duration, hosts):
    token = context.get_token(ctx)

    if not org_id:
        tok = token_parser.Token(token)
        if tok.hasRole("urn:api:agilicus:traffic-tokens", "owner"):
            org_id = tok.getOrg()

    hosts = json.loads(hosts)
    aud = [
        "urn:api:agilicus:gateway",
        "urn:api:agilicus:users",
        "urn:api:agilicus:applications",
    ]
    return _create_token(
        ctx, user_id, duration, aud=aud, hosts=hosts, org_id=org_id
    ).text


def create_token(ctx, user_id, roles, duration, audiences, org_id, scopes=None):
    result = _create_token(
        ctx, user_id, duration, aud=audiences, roles=roles, org_id=org_id, scopes=scopes
    )
    if result.status_code != 200:
        print(f"Unable to retrieve token: {result.status_code} ({result.text})")
        return None
    return result.text


def _get_service_access_token(auth_doc, expiry=None):
    doc_id = auth_doc["metadata"]["id"]
    iss = f"urn:agilicus:authentication_documents:{doc_id}"

    if expiry is None:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    token = {
        "audience": "urn:api:agilicus:tokens",
        "issuer": iss,
        "user_id": auth_doc["spec"]["user_id"],
        "org_id": auth_doc["spec"]["org_id"],
        "expiry": str(expiry),
    }

    return jwt.encode(token, key=auth_doc["status"]["key"], algorithm="ES256").decode()


def create_service_token(auth_doc, expiry=None, ctx=None, verify=None, **kwargs):

    token = _get_service_access_token(auth_doc, expiry=expiry)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Content-type"] = "application/x-www-form-urlencoded"

    update_if_present(headers, "referer", **kwargs)

    data = {}
    data["grant_type"] = "urn:agilicus:params:oauth:grant-type:identity_statement"

    if ctx:
        data["client_id"] = context.get_client_id(ctx)
        _verify = context.get_cacert(ctx)

    update_if_present(data, "client_id", **kwargs)
    update_if_present(data, "scope", **kwargs)

    if verify:
        _verify = verify

    data["authentication_document_id"] = auth_doc["metadata"]["id"]
    data["identity_assertion"] = token
    url = auth_doc["spec"]["auth_issuer_url"]
    resp = requests.post(url + "/token", headers=headers, data=data, verify=_verify)
    response.validate(resp)
    return resp.text


def query_tokens(
    ctx,
    limit=None,
    expired_from=None,
    expired_to=None,
    issued_from=None,
    issued_to=None,
    org_id=None,
    jti=None,
    sub=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}
    if limit:
        params["limit"] = limit
    if expired_from:
        params["exp_from"] = expired_from
    if expired_to:
        params["exp_to"] = expired_to
    if issued_from:
        params["iat_from"] = issued_from
    if issued_to:
        params["iat_to"] = issued_to
    if jti:
        params["jti"] = jti
    if sub:
        params["sub"] = sub
    if org_id:
        params["org"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org"] = org_id

    query = urllib.parse.urlencode(params)
    uri = "/v1/tokens?{}".format(query)
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def format_authentication_document_as_text(info):
    columns = [
        metadata_column("id"),
        spec_column("user_id"),
        spec_column("org_id"),
        spec_column("expiry"),
        status_column("issuer"),
    ]

    return format_table(info, columns)


def list_authentication_documents(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    query_results = apiclient.tokens_api.list_authentication_documents(**kwargs)
    return query_results.authentication_documents


def add_authentication_document(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    spec = agilicus.AuthenticationDocumentSpec(**kwargs)
    model = agilicus.AuthenticationDocument(spec=spec)
    return apiclient.tokens_api.create_authentication_document(model).to_dict()


def _get_auth_doc(ctx, apiclient, document_id, **kwargs):
    keyword_args = {}
    keyword_args["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.get_authentication_document(document_id, **keyword_args)


def show_authentication_document(ctx, document_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_auth_doc(ctx, apiclient, document_id, **kwargs).to_dict()


def delete_authentication_document(ctx, document_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.delete_authentication_document(document_id, **kwargs)


def validate_identity_assertion(ctx, document_id, token, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.IdentityAssertion(
        authentication_document_id=document_id, token=token
    )
    return apiclient.tokens_api.create_authentication_document(model).to_dict()
