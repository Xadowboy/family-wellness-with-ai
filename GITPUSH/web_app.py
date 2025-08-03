#!/usr/bin/env python3
"""
Family Wellness Web App using Streamlit
Users provide their own Google API key
"""

import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(
    page_title="Family Wellness AI Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Personalities
PERSONALITIES = {
    'sage': {
        'name': '🧠 Sage',
        'role': 'Youth Mental Health Counselor',
        'description': 'For teenagers and young adults (mental health, academics)',
        'prompt': """You are Sage, a supportive AI counselor for Indian youth aged 13-25. You understand academic pressure, family expectations, and cultural challenges. Always:
- Provide empathetic, non-judgmental support
- Recognize signs of serious mental health concerns
- Offer practical coping strategies rooted in Indian context
- Bridge communication gaps between youth and families
- Use encouraging, culturally sensitive language"""
    },
    'nurture': {
        'name': '🤱 Nurture',
        'role': 'Parenting Guide',
        'description': 'For parents and guardians (parenting strategies)',
        'prompt': """You are Nurture, an experienced parenting guide for Indian families. You understand diverse family structures, cultural values, and developmental science. Always:
- Provide evidence-based parenting strategies
- Respect cultural traditions while promoting healthy development
- Adapt advice for different socioeconomic contexts
- Support parents' mental health and well-being
- Offer practical, actionable guidance"""
    },
    'spark': {
        'name': '✨ Spark',
        'role': 'Child Development Specialist',
        'description': 'For child development activities and learning',
        'prompt': """You are Spark, a child development specialist creating engaging, age-appropriate activities. You understand Indian cultural contexts and diverse learning needs. Always:
- Design inclusive activities for all abilities
- Incorporate cultural elements and local resources
- Provide clear, step-by-step instructions
- Suggest modifications for special needs
- Make learning fun and engaging"""
    },
    'bridge': {
        'name': '🌉 Bridge',
        'role': 'Family Communication Mediator',
        'description': 'For family communication and conflict resolution',
        'prompt': """You are Bridge, a family communication specialist helping resolve conflicts and improve understanding. Always:
- Remain neutral and understanding
- Suggest practical communication strategies
- Help different generations understand each other
- Provide conflict resolution techniques
- Support healthy family dynamics"""
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'personality' not in st.session_state:
    st.session_state.personality = 'sage'
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False
if 'model' not in st.session_state:
    st.session_state.model = None

def validate_api_key(api_key):
    """Validate Google API key"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        # Test with a simple request
        response = model.generate_content("Hello")
        return True, model
    except Exception as e:
        return False, str(e)

def initialize_chat_session(personality_key):
    """Initialize chat session with selected personality"""
    if not st.session_state.model:
        return False
    
    personality = PERSONALITIES[personality_key]
    st.session_state.chat_session = st.session_state.model.start_chat(
        history=[
            {
                "role": "user",
                "parts": ["Hello, I need help with family wellness and development."]
            },
            {
                "role": "model", 
                "parts": [f"{personality['prompt']}\n\nHello! I'm {personality['name']}, your {personality['role']}. How can I support you today?"]
            }
        ]
    )
    return True

def check_crisis_keywords(message):
    """Check for crisis keywords in user message"""
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hurt myself', 'die', 'worthless']
    return any(keyword in message.lower() for keyword in crisis_keywords)

def get_crisis_response():
    """Return crisis response"""
    return """🚨 I'm concerned about what you've shared. Your feelings are valid, but help is available.

**Please reach out immediately:**
- **India - Suicide Prevention**: 104 (24/7)
- **KIRAN Mental Health**: 1800-599-0019
- **Vandrevala Foundation**: 9999666555
- **iCall Psychosocial Helpline**: 9152987821

You don't have to face this alone. Would you like to talk about what's making you feel this way?"""

# Main app
st.title("🏠 Family Wellness AI Platform")
st.markdown("*Powered by Google Gemini AI - Bring Your Own API Key*")

# API Key Setup
if not st.session_state.api_key_valid:
    st.markdown("---")
    st.header("🔑 Setup Your API Key")
    
    with st.expander("📝 How to Get Your Google API Key", expanded=True):
        st.markdown("""
        **Follow these steps to get your free Google API key:**
        
        1. **Visit Google AI Studio**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
        2. **Sign in** with your Google account
        3. **Click "Create API Key"**
        4. **Copy the generated key**
        5. **Paste it in the field below**
        
        **Note**: Your API key is stored only in your browser session and is not saved anywhere else.
        """)
    
    # API Key Input
    api_key = st.text_input(
        "Enter your Google API Key:",
        type="password",
        help="Your API key will only be used for this session and won't be stored."
    )
    
    if st.button("🚀 Validate & Start"):
        if api_key:
            with st.spinner("Validating your API key..."):
                is_valid, result = validate_api_key(api_key)
                
                if is_valid:
                    st.session_state.api_key_valid = True
                    st.session_state.model = result
                    st.success("✅ API key validated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Invalid API key: {result}")
        else:
            st.warning("⚠️ Please enter your API key first.")
    
    # Info about costs
    st.info("""
    **💡 About API Costs:**
    - Google Gemini API has a generous free tier
    - Free tier includes thousands of requests per month
    - Perfect for personal and family use
    - No charges for typical usage patterns
    """)
    
    st.stop()

# Main application (only shown after API key validation)
col1, col2 = st.columns([1, 3])

# Sidebar functionality in column 1
with col1:
    st.header("🤖 AI Assistants")
    
    # Personality selection
    personality_options = {key: f"{value['name']}\n{value['description']}" 
                          for key, value in PERSONALITIES.items()}
    
    for key, personality in PERSONALITIES.items():
        if st.button(
            f"{personality['name']}\n{personality['description']}", 
            key=key,
            use_container_width=True
        ):
            if key != st.session_state.personality:
                st.session_state.personality = key
                st.session_state.messages = []
                st.session_state.chat_session = None
                st.rerun()
    
    st.markdown("---")
    
    # Quick Assessment
    with st.expander("📊 Quick Assessment"):
        age_group = st.selectbox("Age Group:", 
                                ["13-17", "18-25", "Parent/Guardian", "Other"])
        concern = st.selectbox("Primary Concern:", 
                              ["Mental health", "Academic stress", "Parenting", 
                               "Child development", "Family communication"])
        mood = st.slider("Current mood (1-10):", 1, 10, 5)
        
        if st.button("Get Recommendation", key="assess"):
            if age_group in ["13-17", "18-25"] and concern in ["Mental health", "Academic stress"]:
                rec_personality = 'sage'
            elif age_group == "Parent/Guardian" and concern in ["Parenting", "Child development"]:
                rec_personality = 'nurture'
            elif concern == "Child development":
                rec_personality = 'spark'
            else:
                rec_personality = 'bridge'
            
            if rec_personality != st.session_state.personality:
                st.session_state.personality = rec_personality
                st.session_state.messages = []
                st.session_state.chat_session = None
                st.success(f"Switched to {PERSONALITIES[rec_personality]['name']}")
                st.rerun()
    
    st.markdown("---")
    
    # Crisis Resources
    with st.expander("🆘 Crisis Resources"):
        st.markdown("""
        **India:**
        - Suicide Prevention: 104
        - KIRAN Mental Health: 1800-599-0019
        - Vandrevala Foundation: 9999666555
        - iCall: 9152987821
        
        **Emergency:**
        - Police: 100
        - Ambulance: 108
        - Women Helpline: 181
        """)
    
    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()
    
    # Reset API Key
    if st.button("🔄 Change API Key", use_container_width=True):
        st.session_state.api_key_valid = False
        st.session_state.model = None
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# Chat interface in column 2
with col2:
    current_personality = PERSONALITIES[st.session_state.personality]
    
    st.subheader(f"💬 Chat with {current_personality['name']}")
    st.caption(f"Your {current_personality['role']}")
    
    # Initialize chat session if needed
    if st.session_state.chat_session is None:
        if initialize_chat_session(st.session_state.personality):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Hello! I'm {current_personality['name']}, your {current_personality['role']}. How can I support you today?"
            })
    
    # Chat container
    chat_container = st.container(height=400)
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Check for crisis keywords
        if check_crisis_keywords(prompt):
            response = get_crisis_response()
        else:
            # Generate AI response
            try:
                with st.spinner("Thinking..."):
                    context_prompt = f"""As {current_personality['name']}, a {current_personality['role']}, respond to: {prompt}
                    
                    Remember: {current_personality['prompt']}"""
                    
                    ai_response = st.session_state.chat_session.send_message(context_prompt)
                    response = ai_response.text
            except Exception as e:
                response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        
        # Display AI response
        with chat_container:
            with st.chat_message("assistant"):
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌟 Family Wellness & Development Platform | Users Provide Their Own API Keys</p>
    <p>🔐 Your API key is secure and only used during your session</p>
    <p>Remember: Taking care of your family's mental health is a journey, not a destination.</p>
</div>
""", unsafe_allow_html=True)