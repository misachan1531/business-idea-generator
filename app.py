import streamlit as st
import requests
import json

class BusinessIdeaGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.perplexity.ai/chat/completions"

    def generate_ideas(self, user_inputs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Generate 5 business ideas based on:
        Budget: {user_inputs['budget']}
        Skills: {user_inputs['skills']}
        Interests: {user_inputs['interests']}
        Location: {user_inputs['location']}
        
        For each idea, provide:
        1. Business concept
        2. Setup requirements
        3. Potential challenges
        4. Estimated ROI timeline
        5. Key success factors
        6. Marketing strategies
        7. Scaling potential
        
        Format each idea clearly with headings and bullet points.
        """

        data = {
            "model": "sonar-pro",  # Updated to correct model
            "messages": [
                {
                    "role": "system",
                    "content": "You are an experienced business consultant specializing in helping entrepreneurs identify viable business opportunities."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Error: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="Business Idea Generator", layout="wide")
    
    st.title("💡 Business Idea Generator")
    st.markdown("Generate personalized business ideas based on your preferences")
    
    # Model selection and API key input
    with st.sidebar:
        st.header("Configuration")
        model = st.selectbox(
            "Select Model",
            [
                "sonar-pro",
                "sonar",
                "sonar-deep-research",
                "sonar-reasoning-pro",
                "sonar-reasoning",
                "r1-1776"
            ]
        )
        api_key = st.text_input("Enter Perplexity API Key", type="password")
        
        # Add model information
        st.info("""
        Model Information:
        - sonar-pro: 200k context length
        - sonar: 128k context length
        - sonar-deep-research: 60k context length
        - sonar-reasoning-pro: 128k context length
        - sonar-reasoning: 128k context length
        - r1-1776: 128k context length
        """)
    
    # Main input form
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.selectbox(
            "💰 Investment Budget",
            [
                "Under $1,000",
                "$1,000-$5,000",
                "$5,000-$10,000",
                "$10,000-$50,000",
                "Over $50,000"
            ]
        )
        skills = st.text_area(
            "🎯 Your Skills/Experience",
            placeholder="E.g., programming, marketing, teaching..."
        )
    
    with col2:
        interests = st.text_area(
            "💫 Your Interests/Passions",
            placeholder="E.g., technology, health, arts..."
        )
        location = st.text_input(
            "📍 Location",
            placeholder="City, Country"
        )

    # Additional preferences
    with st.expander("Additional Preferences (Optional)"):
        time_commitment = st.selectbox(
            "Time Commitment",
            ["Full-time", "Part-time", "Flexible"]
        )
        market_preference = st.multiselect(
            "Target Market",
            ["Local", "National", "International", "Online"]
        )

    if st.button("Generate Business Ideas 🚀"):
        if not api_key:
            st.error("Please enter your API key in the sidebar")
            return
            
        if not all([skills, interests, location]):
            st.warning("Please fill in all required fields")
            return
            
        with st.spinner("Generating innovative business ideas..."):
            generator = BusinessIdeaGenerator(api_key)
            user_inputs = {
                "budget": budget,
                "skills": skills,
                "interests": interests,
                "location": location,
                "time_commitment": time_commitment if time_commitment else "Not specified",
                "market_preference": ", ".join(market_preference) if market_preference else "Not specified"
            }
            
            result = generator.generate_ideas(user_inputs)
            
            if "Error" in result:
                st.error(result)
            else:
                st.success("✨ Business Ideas Generated Successfully!")
                
                # Display results in a nice format
                st.markdown("### 🎯 Your Personalized Business Ideas")
                st.markdown(result)
                
                # Download button
                st.download_button(
                    "📥 Download Ideas",
                    result,
                    "business_ideas.txt",
                    "text/plain"
                )

    # Tips section
    with st.expander("💡 Tips for Success"):
        st.markdown("""
        - Research your target market thoroughly
        - Start small and test your concept
        - Focus on solving real problems
        - Network with other entrepreneurs
        - Keep track of your expenses
        - Stay flexible and adapt to feedback
        """)

if __name__ == "__main__":
    main()