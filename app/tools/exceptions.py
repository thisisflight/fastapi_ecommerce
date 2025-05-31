from app import exceptions

exception_handlers = {
    exceptions.UserPermissionError: {"status_code": 403, "detail": "User does not have permission"},
    exceptions.UserAlreadyExists: {"status_code": 409, "detail": "User already exists"},
    exceptions.UserNotFoundError: {"status_code": 404, "detail": "User not found"},
    exceptions.ProductNotFoundError: {"status_code": 404, "detail": "Product not found"},
    exceptions.InvalidCredentialsError: {"status_code": 401, "detail": "Invalid credentials"},
    exceptions.WrongUsernameCredentialsError: {
        "status_code": 401,
        "detail": "Wrong username",
    },
    exceptions.InactiveUserError: {"status_code": 401, "detail": "User is inactive"},
    exceptions.CategoryNotFoundError: {"status_code": 404, "detail": "Category not found"},
    exceptions.ReviewNotFoundError: {"status_code": 404, "detail": "Review not found"},
    exceptions.ReviewAlreadyExists: {
        "status_code": 409,
        "detail": "User already has a review for this product",
    },
}
