from mest import Mest

mest = Mest()

if __name__ == '__main__':
    mest.run()

# Now, you can run a simple POST request!
"""
curl -X POST http://localhost:1234/api/v1/predict \
-H 'Content-Type: application/json' \
  -d '{
    "feature1": 10,
    "feature2": 4,
    "feature3": 0.123
}'
"""
