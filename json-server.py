import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import (
    login_user,
    create_user,
    get_posts_by_user,
    get_post_by_id,
    get_categories,
    update_post,
    get_all_posts,
    create_post,
    delete_post,
    get_user_by_id,
)


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Rare Publishing"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = get_post_by_id(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            if "user_id" in url["query_params"]:
                user_id = url["query_params"]["user_id"][0]
                response_body = get_posts_by_user(user_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            else:
                response_body = get_all_posts()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            response_body = get_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = get_user_by_id(url["pk"])
                if response_body is None:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )

                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        """Handle POST requests from a client"""
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("Content-Length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "login":
            res = login_user(request_body)
            return self.response(
                res,
                status.HTTP_201_SUCCESS_CREATED.value,
            )

        if url["requested_resource"] == "register":
            res = create_user(request_body)
            return self.response(
                res,
                status.HTTP_201_SUCCESS_CREATED.value,
            )

        if url["requested_resource"] == "posts":
            res = create_post(request_body)
            return self.response(
                res,
                status.HTTP_201_SUCCESS_CREATED.value,
            )

    def do_DELETE(self):
        """Handle DELETE requests for a single resource"""
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                return self.response(
                    "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                )

        # if url["requested_resource"] == "orders":
        #     if pk != 0:
        #         successfully_deleted = delete_order(pk)
        #         if successfully_deleted:
        #             return self.response(
        #                 "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
        # #             )
        #         return self.response(
        #             "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        #         )

    def do_PUT(self):
        """Handle PUT requests from a client"""

        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                success = update_post(url["pk"], request_body)
                if success:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
            else:
                return self.response(
                    "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                )

        # if url["requested_resource"] == "metals":
        #     if pk != 0:
        #         successfully_updated = update_metal(pk, request_body)
        #         if successfully_updated:
        #             return self.response(
        #                 "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
        #             )
        #         else:
        #             return self.response(
        #                 "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        # #             )
        #     else:
        #         return self.response(
        #             "", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
        #         )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
