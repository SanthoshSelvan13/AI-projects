from google import genai

# Create client with your API key
client = genai.Client(api_key="AIzaSyA1ePzw81K5e7u1Bhx3GmOSXsZ-phKGeho")

# Generate content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain machine learning in one line"
)

print(response.text)