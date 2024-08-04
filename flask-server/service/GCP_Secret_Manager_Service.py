class GCP_Secret_Manager_Service(object):
    def __init__(self) -> None:
        self.project_id = "nourish-351123"

    def get_secret_version(self, secret_id) -> str:
        """
        Get information about the given secret version. It does not include the
        payload data.
        """

        # Import the Secret Manager client library.
        from google.cloud import secretmanager

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"

        # Get the latest secret version.
        response = client.get_secret_version(request={"name": name})

        # Parse the response.
        version = response.name.split("/")[-1]
        return version

    def get_secret(self, secret_id) -> str:
        """
        Get information about the given secret. This only returns metadata about
        the secret container, not any secret material.
        """

        # Import the Secret Manager client library.
        from google.cloud import secretmanager

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret.
        secret_path = client.secret_version_path(
            self.project_id, secret_id, self.get_secret_version(secret_id)
        )

        # Get the secret.

        response = client.access_secret_version(request={"name": secret_path})

        # Access the secret payload.
        secret_string = response.payload.data.decode("UTF-8")
        return secret_string
