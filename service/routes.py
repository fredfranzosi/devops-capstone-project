"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns a list of Accounts"""
    app.logger.info("Request to list Accounts...")

    accounts = []
    app.logger.info("Find all")
    accounts = Account.all()

    results = [acc.serialize() for acc in accounts]
    app.logger.info("[%s] Accounts returned", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """
    Read an Account
    This endpoint will read an Account with the given product_id
    """
    app.logger.info("Request to Read an Account with ID %s.", account_id)

    # use the Account.find() method to find the account
    found_account = Account.find(account_id)

    # abort() with a status.HTTP_404_NOT_FOUND if it cannot be found
    if not found_account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with {account_id} not found",
        )

    # return the serialize() version of the account with a return code of status.HTTP_200_OK
    return found_account.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Updates an Account
    This endpoint will update an Account
    """
    app.logger.info("Request to Update an Account with ID %s.", account_id)

    check_content_type("application/json")

    found_account = Account.find(account_id)

    # Abort with a return code HTTP_404_NOT_FOUND if the account was not found.
    if not found_account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with {account_id} not found",
        )

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    account = Account()
    account.deserialize(data)
    account.id = account_id
    account.update()
    app.logger.info("Account with  id [%s] updated!", account.id)

    return account.serialize(), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Deletes an Account
    This endpoint will delete an Account with the given account_id
    """
    app.logger.info("Request to DELETE an Account with ID %s.", account_id)

    # Call the Account.find() method which will return an account with the given account_id.
    found_account = Account.find(account_id)

    # Abort with a return code HTTP_404_NOT_FOUND if the product was not found.
    if not found_account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with ID = {account_id} not found",
        )

    found_account.delete()
    app.logger.info("Account with  id [%s] deleted!", found_account.id)

    return '', status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
