import os

# Coupon code for balance check tests
# Comes from .env, with a safe default for local runs
COUPON_CODE = os.getenv("TEST_COUPON_CODE", "1234-1234-1234")
