# coding: utf-8
#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.



"""
     <i>Fecha de creación: 6 de diciembre, 2019</i>

     author: Saintiago García
     version: 1.0
"""
import sys
import unittest
import warnings
from datetime import timedelta

from wire4_client import ContactoApi, ContactRequest, CepSearchBanxico, ComprobanteElectrnicoDePagoCEPApi, \
    CepResponse, SuscripcionesApi, PreEnrollmentData, PreEnrollmentResponse, CuentasDeBeneficiariosSPEIApi, \
    RelationshipsResponse, AccountRequest, Account, Person, TokenRequiredResponse, BeneficiariesResponse, \
    AmountRequest, InstitucionesApi, InstitutionsList, SaldoApi, BalanceListResponse, CuentasDeBeneficiariosSPIDApi, \
    SpidClassificationsResponseDTO, TransferenciasSPIDApi, AccountSpid, BeneficiaryInstitution, DepositantesApi, \
    DepositantsRegister, DepositantsResponse, TransferenciasSPEIApi, WebhooksApi, WebhooksList, WebhookResponse, \
    Billing, FacturasApi, WebhookRequest, TransactionOutgoingSpid, TransactionsOutgoingRegister, TransactionOutgoing, \
    EmpresasCoDiApi, PuntosDeVentaCoDiApi, OperacionesCoDiApi, CompanyRequested, CertificateRequest, SalesPointRequest, \
    PeticionesDePagoPorCoDiApi, CodiCodeRequestDTO, CodiOperationsFiltersRequestDTO, ContractsDetailsApi, \
    ContractDetailRequest, PreMonexAuthorization, UrlsRedirect, AuthorizationTransactionGroup
from wire4_client.rest import ApiException

from wire4_auth.auth.oauth_wire4 import OAuthWire4
from wire4_auth.core.environment_enum import EnvironmentEnum


# noinspection DuplicatedCode
class TestAccount(unittest.TestCase):

    CLIENT_ID: str = "FxUWmqYGZuv8O1qjxstvIyJothMa"

    CLIENT_SECRET: str = "kjwbkrPVgXsnaUGzthj55dsFhx4a"

    SUBSCRIPTION: str = "f1504fea-3a8f-475a-a50a-90d3c40efc59"

    USER_KEY: str = "071e2b59b354186b3a0158de493536@sandbox.wire4.mx"

    SECRET_KEY: str = "0d1e33e94604f01b4e00d2fcb6b48f"

    SALES_POINT_ID='58b8365c-80a1-4c5c-88cd-b3ec9f2b1383'

    SALES_POINT_USER_KEY='9add3923dbb4129be8c3be1fdbeaaf@develop.wire4.mx'

    SALES_POINT_USER_SECRET = 'b7b2c43924f4612817261899eff42f'

    AMBIENT: EnvironmentEnum = EnvironmentEnum.DEVELOPMENT

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        pass

    def testSendContact(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = ContactoApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info: types, required fields, etc.)
        body = ContactRequest(address="Calle Falsa 123, Col Fantasía", company="Compu Mundo Hiper Mega Red",
                              contact_person="Homer J Simpson", email="homer.simpson@compumundohipermegared.com",
                              phone_number="4422102030")

        try:
            response = api_instance.send_contact_using_post_with_http_info(body, oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainCep(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = ComprobanteElectrnicoDePagoCEPApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info: types, required fields, etc.)
        body = CepSearchBanxico(amount="8963.25", beneficiary_account="072680004657656853",
                                beneficiary_bank_key="40072", clave_rastreo="58735618", operation_date="05-12-2018",
                                reference="1122334", sender_account="112680000156896531", sender_bank_key="40112")

        try:
            response: CepResponse = api_instance.obtain_transaction_cep_using_post(body, oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testMakePreSubscription(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = SuscripcionesApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info: types, required fields, etc.)
        body = PreEnrollmentData(cancel_return_url="https://your-app-url.mx/return",
                                 return_url="https://your-app-url.mx/cancel")

        try:
            response: PreEnrollmentResponse = api_instance.pre_enrollment_monex_user_using_post(body, oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testDeletePreSubscription(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = SuscripcionesApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = "570c9ca4-c05a-4c4a-a783-8ce5d57c46af"

        try:
            response = api_instance.remove_subscription_pending_status_using_delete_with_http_info(oauth_token_app,
                                                                                                   subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testDeleteSubscription(self):

        subscription_to_remove_user_key = "e9ab95ee3234664b06f2217243ab36@sandbox.wire4.mx"
        subscription_to_remove_user_secret = "7a594a437e34747b7cd720ad8c9925"

        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            # The user_key and user_secret belongs to the subscription to delete
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                subscription_to_remove_user_key, subscription_to_remove_user_secret, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = SuscripcionesApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = "88e2f2ef-c8a7-46fd-94dd-65a1d5dc4f08"

        try:
            response = api_instance.remove_enrollment_user_using_delete_with_http_info(oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainRelationships(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: RelationshipsResponse = api_instance.get_available_relationships_monex_using_get(
                oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testPreRegisterBeneficiaries(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        body: AccountRequest = AccountRequest(return_url="https://your-app-url.mx/return",
                                              cancel_return_url="https://your-app-url.mx/cancel",
                                              accounts=[Account(amount_limit=10000.00,
                                                                beneficiary_account="112680000156896531",
                                                                email=["beneficiary@wire4.mx"],
                                                                kind_of_relationship="RECURRENTE",
                                                                numeric_reference_spei="1234567",
                                                                payment_concept_spei="concept spei",
                                                                person=Person(last_name="Simpson",
                                                                              middle_name="Jay",
                                                                              name="Bartolomeo"),
                                                                relationship="ACREEDOR",
                                                                rfc="SJBA920125AB1")])

        try:
            response: TokenRequiredResponse = api_instance.pre_register_accounts_using_post(
                body, oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRemoveBeneficiariesPending(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        request_id: str = "c46bfb5f-c9e0-4f5a-9b7c-2ec0c5f708ff"

        try:
            response = api_instance.remove_beneficiaries_pending_using_delete_with_http_info(
                oauth_token_user, request_id, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainBeneficiaries(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            # for filter by RFC:
            # api_instance.get_beneficiaries_for_account_using_get(oauth_token_user, subscription, rfc="RFCE010980AR3")
            #
            # for filter by account:
            # api_instance.get_beneficiaries_for_account_using_get(
            #       oauth_token_user, subscription,account="112680000156896531")
            #
            # for filter by RFC and account:
            # api_instance.get_beneficiaries_for_account_using_get(oauth_token_user, subscription,
            #       rfc="RFCE010980AR3", account="112680000156896531")
            response: BeneficiariesResponse = api_instance.get_beneficiaries_for_account_using_get(
                oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainBeneficiariesByRequestId(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        request_id: str = "0726a947-deaf-4bdc-a411-dc40192c78d9"

        try:
            # authorization, request_id, subscription
            response: BeneficiariesResponse = api_instance.get_beneficiaries_by_request_id(
                oauth_token_user, request_id, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testChangeAmountLimitBeneficiary(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        account: str = "021680064490682994"
        body: AmountRequest = AmountRequest(amount_limit=20000.00, currency_code="MXP",
                                            previous_amount_limit=10000.00, return_url="https://your-app-url.mx/return",
                                            cancel_return_url="https://your-app-url.mx/cancel",)

        try:
            response = api_instance.update_amount_limit_account_using_put(body, oauth_token_user, account, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testDeleteBeneficiary(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        account: str = "044680035044988526"

        try:
            response = api_instance.delete_account_using_delete_with_http_info(oauth_token_user, account, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainInstitutions(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = InstitucionesApi(oauth_wire.get_default_api_client())

        try:
            response: InstitutionsList = api_instance.get_all_institutions_using_get(oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainBalance(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = SaldoApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: BalanceListResponse = api_instance.get_balance_using_get(oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def test_multiple(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spid_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPIDApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            print("oauth_token_user 1" + oauth_token_user)
            response: SpidClassificationsResponseDTO = api_instance.get_spid_classifications_using_get(
                oauth_token_user, subscription)
            print(response)

            print("\n")
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
            print("oauth_token_user 2" + oauth_token_user)
            response: SpidClassificationsResponseDTO = api_instance.get_spid_classifications_using_get(
                oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainSPIDClassifications(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spid_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPIDApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: SpidClassificationsResponseDTO = api_instance.get_spid_classifications_using_get(
                oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testPreRegisterBeneficiariesSPID(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spid_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPIDApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        body: AccountSpid = AccountSpid(return_url="https://your-app-url.mx/return",
                                        cancel_return_url="https://your-app-url.mx/cancel",
                                        amount_limit=1000.00,
                                        beneficiary_account="112680000156896531",
                                        email=["beneficiary.spid@wire4.mx"],
                                        institution=BeneficiaryInstitution(name="Compu Mundo Hiper Mega Red"),
                                        kind_of_relationship="RECURRENTE",
                                        numeric_reference="1234567",
                                        payment_concept="concept spid",
                                        relationship="ACREEDOR",
                                        rfc="SJBA920125AB1")

        try:
            response: TokenRequiredResponse = api_instance.pre_register_accounts_using_post1(
                body=body, authorization=oauth_token_user, subscription=subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testObtainBeneficiariesSpid(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spid_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPIDApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            # for filter by RFC:
            # api_instance.get_spid_beneficiaries_for_account(oauth_token_user, subscription, rfc="RFCE010980AR3")
            #
            # for filter by account:
            # api_instance.get_spid_beneficiaries_for_account(
            #       oauth_token_user, subscription, account="112680000156896531")
            #
            # for filter by RFC and account:
            # api_instance.get_spid_beneficiaries_for_account(oauth_token_user,
            #       subscription, rfc="RFCE010980AR3", account="112680000156896531")
            response: BeneficiariesResponse = api_instance.get_spid_beneficiaries_for_account(
                oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testGetDepositants(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = DepositantesApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: BalanceListResponse = api_instance.get_depositants_using_get(oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRegisterDepositants(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = DepositantesApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        body: DepositantsRegister = DepositantsRegister(alias="Depositant 0292921",
                                                        currency_code="MXP",
                                                        email=["depositant@wire4.mx"],
                                                        name="Marge Bouvier")

        try:
            response: DepositantsResponse = api_instance.register_depositants_using_post(
                body, oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testIncomingSpeiTransactionsReport(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: list = api_instance.incoming_spei_transactions_report_using_get(oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testOutgoingSpeiTransactionsReport(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION

        try:
            response: list = api_instance.outgoing_spei_transactions_report_using_get(oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRegisterOutgoingSpeiTransaction(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        body: TransactionsOutgoingRegister = TransactionsOutgoingRegister(
                                                                  return_url="https://your-app-url.mx/return",
                                                                  cancel_return_url="https://your-app-url.mx/cancel",
                                                                  transactions=[TransactionOutgoing(
                                                                      order_id="ffdd653a-c250-4b37-be72-b909f480e97b",
                                                                      amount=1259.69,
                                                                      beneficiary_account="112680000156896531",
                                                                      currency_code="MXP",
                                                                      email=["notificar@wire4.mx"],
                                                                      reference=1234567,
                                                                      concept="Transfer out test 1")])

        try:
            response: TokenRequiredResponse = api_instance.register_outgoing_spei_transaction_using_post(
                body, oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testOutCommingSpeiReportByRequestID(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        request_id = '4d633b1d-1b36-425a-8758-2bebcb657e98'  # str | Identificador de la petición a buscar
        subscription = self.SUBSCRIPTION  # str | El identificador de la suscripción a esta API

        try:
            api_response = api_instance.out_comming_spei_request_id_transactions_report_using_get(oauth_token_user,
                                                                                                  request_id,
                                                                                                  subscription)
            print(api_response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in request
            return

    def testDeleteOutgoingPendingSpeiTransaction(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spei_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        request_id: str = "eca366bb-41eb-440b-8922-d3d9d9edbf80"

        try:
            response: TokenRequiredResponse = api_instance.drop_transactions_pending_using_delete_with_http_info(
                oauth_token_user, request_id, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRegisterOutgoingSpidTransaction(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use password flow and scope "spid_admin"
            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spid_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPIDApi(oauth_wire.get_default_api_client())

        # build body with info (check references for more info, types, required fields)
        subscription: str = self.SUBSCRIPTION
        body: TransactionOutgoingSpid = TransactionOutgoingSpid(return_url="https://your-app-url.mx/return",
                                                                cancel_return_url="https://your-app-url.mx/cancel",
                                                                amount=1259.69,
                                                                beneficiary_account="112680000156896531",
                                                                classification_id="01",
                                                                currency_code="USD",
                                                                email=["notificar@wire4.mx"],
                                                                numeric_reference_spid=1234567,
                                                                order_id="239474bf-4c4f-4f19-b63b-51ee39e9f4e0",
                                                                payment_concept_spid="Transfer out test 1")

        try:
            response: TokenRequiredResponse = api_instance.register_outgoing_spid_transaction_using_post(
                body, oauth_token_user, subscription)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRegisterWebHook(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = WebhooksApi(oauth_wire.get_default_api_client())
        body: WebhookRequest = WebhookRequest(events=["ACCOUNT.CREATED",
                                                      "TRANSACTION.OUTGOING.RECEIVED",
                                                      "ENROLLMENT.CREATED"],
                                              name="SDK-WEBHOOK-REGISTER",
                                              url="https://www.webhook.site/39034a03-8faf-424e-bb4a-7c3fee2bbfd3")

        try:
            response: WebhookResponse = api_instance.register_webhook(body, oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testGetWebHooks(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = WebhooksApi(oauth_wire.get_default_api_client())

        try:
            response: WebhooksList = api_instance.get_webhooks(oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testGetWebHookById(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = WebhooksApi(oauth_wire.get_default_api_client())

        try:
            response: WebhookResponse = api_instance.get_webhook(id="wh_3fe3e5f4849f4cabb147804fd55c86fc",
                                                                 authorization=oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testGetFacturas(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = FacturasApi(oauth_wire.get_default_api_client())

        try:
            response: list = api_instance.billings_report_using_get(authorization=oauth_token_app, period="2019-10")
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testGetFacturasById(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = FacturasApi(oauth_wire.get_default_api_client())

        try:
            response: Billing = api_instance.billings_report_by_id_using_get(authorization=oauth_token_app,
                                                                             id="834BA74A-BBBB-43C4-8400-A4528153C2BD")
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testAuthorizeAccountsPendingPUT(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "spei_admin"

            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            print(ex)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = CuentasDeBeneficiariosSPEIApi(oauth_wire.get_default_api_client())

        try:
            response: Billing = api_instance.authorize_accounts_pending_put(body=UrlsRedirect(cancel_return_url='https://patito.cafe/cancel/return',
                                                                                              return_url='https://patito.cafe/return'),
                                                                            authorization=oauth_token_user,
                                                                            subscription=self.SUBSCRIPTION)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testCreateAuthorizationTransactionsGroup(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)

        try:
            # Obtain an access token use application flow and scope "spei_admin"

            oauth_token_user: str = oauth_wire.obtain_access_token_app_user(
                self.USER_KEY, self.SECRET_KEY, "spei_admin")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            print(ex)
            # Optional manage exception in access token flow
            return

        # create an instance of the API class and add the bearer token to request
        api_instance = TransferenciasSPEIApi(oauth_wire.get_default_api_client())

        try:
            request_body =AuthorizationTransactionGroup(redirect_urls=UrlsRedirect(cancel_return_url='http://patito.cafe/cancel/return',
                                                                                   return_url='http://patito.cafe/return'),
                                                        transactions=['dd919bdc-a71c-449d-82ff-5d0535b28984',
                                                                      'dd919bdc-a71c-449d-82ff-5d0535b28984'])
            response: Billing = api_instance.create_authorization_transactions_group(body=request_body,
                                                                                     authorization=oauth_token_user,
                                                                                     subscription=self.SUBSCRIPTION)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return

        pass

    def testRegisterCompanyUsingPOST(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("codi_general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = EmpresasCoDiApi(oauth_wire.get_default_api_client())

        try:
            certificate = CertificateRequest("0000010000100002800", "0000010000100002800", 9,
                               'koadklasjdlajlsldikaa5d4a5sd54a5sda2s1d5asd4a5sx1a5sd41as5d4as56d456g465gh45hjk46uy54h56df456sdf4s56df4s6df4s6d5f2xzc15sdf46sd4a654d2zxc1ds56')
            companyRequest= CompanyRequested("Servicios especializados Patito Cafe",certificate , "Servicios Patito Cafe",
                             'MAG041126GT8')
            response = api_instance.register_company_using_post(companyRequest, oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testObtainCompanies(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("codi_general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = EmpresasCoDiApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.obtain_companies(oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testCreateSalesPoint(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("codi_general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = PuntosDeVentaCoDiApi(oauth_wire.get_default_api_client())

        try:
            access_ip = '198.168.0.1'
            cable_account = '102211123456789141'
            name = 'Sucursales Centro Sur'
            notifications_url = 'https://patito.requestcatcher.com/'
            body = SalesPointRequest(access_ip, cable_account, name, notifications_url)
            company_id = '1d49fa2f-40f9-4d0b-8a7b-164df9d2a452'
            response = api_instance.create_sales_point(body, oauth_token_app, company_id)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testObtainSalesPoints(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("codi_general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = PuntosDeVentaCoDiApi(oauth_wire.get_default_api_client())

        try:
            company_id = '1d49fa2f-40f9-4d0b-8a7b-164df9d2a452'
            response = api_instance.obtain_sale_points(oauth_token_app,company_id)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testGenerateCodiCodeQR(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_admin"
            oauth_token_app_user: str = oauth_wire.obtain_access_token_app_user(self.SALES_POINT_USER_KEY, self.SALES_POINT_USER_SECRET, 'codi_admin')
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = PeticionesDePagoPorCoDiApi(oauth_wire.get_default_api_client())

        try:

            body = CodiCodeRequestDTO(amount=6500.00, concept='Pago de servicios mes anterior', due_date='2020-08-29T15:45:00',
                                      order_id='order_num_12AA', phone_number='5500000001', type='PUSH_NOTIFICATION')
            response = api_instance.generate_codi_code_qr(body,oauth_token_app_user,self.SALES_POINT_ID)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testConsultCodiRequestByOrderId(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_admin"
            oauth_token_app_user: str = oauth_wire.obtain_access_token_app_user(self.SALES_POINT_USER_KEY,
                                                                                self.SALES_POINT_USER_SECRET,
                                                                                'codi_admin')
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = PeticionesDePagoPorCoDiApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.consult_codi_request_by_order_id(authorization=oauth_token_app_user,
                                                                     order_id='order_num_12AA',sales_point_id=self.SALES_POINT_ID)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testConsultCodiOperations(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "codi_report"
            oauth_token_app_user: str = oauth_wire.obtain_access_token_app_user(self.SALES_POINT_USER_KEY,
                                                                                self.SALES_POINT_USER_SECRET,
                                                                                'codi_report')
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = OperacionesCoDiApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.consult_codi_operations(oauth_token_app_user, sales_point_id=self.SALES_POINT_ID,
                                                            page=0, size=20, body=CodiOperationsFiltersRequestDTO())
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testObtainContractDetails(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = ContractsDetailsApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.obtain_contract_details(body=ContractDetailRequest(contract='32154',
                                                                                       password='123Fake?',
                                                                                       token_code='12345',
                                                                                       user_name='dgonzalez'),
                                                            authorization=oauth_token_app, x_access_key='123Fake?')
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testCreateAuthorization(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = ContractsDetailsApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.create_authorization(body=PreMonexAuthorization(business_name="Central Patito Cafe",
                                                                                    cancel_return_url='https://patito.cafe/cancel',
                                                                                    return_url='https://patito.cafe/return',
                                                                                    rfc='VOC990129I26'),
                                                         authorization=oauth_token_app)
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass

    def testObtainAuthorizedUsers(self):
        # Create the authenticator to obtain access token
        # The token URL and Service URL are defined for this environment enum value.
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        try:
            # Obtain an access token use application flow and scope "general"
            oauth_token_app: str = oauth_wire.obtain_access_token_app("general")
        except ApiException as ex:
            print("Exception to obtain access token %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        api_instance = ContractsDetailsApi(oauth_wire.get_default_api_client())

        try:
            response = api_instance.obtain_authorized_users(authorization=oauth_token_app,x_access_key='123Fake?',
                                                            request_id='4a867c6d-3787-4987-bdd6-8018a97ed87d')
            print(response)
        except ApiException as ex:
            print("Exception when calling the API %s\n" % ex, file=sys.stderr)
            # Optional manage exception in access token flow
            return
        pass


if __name__ == '__main__':
    unittest.main()
