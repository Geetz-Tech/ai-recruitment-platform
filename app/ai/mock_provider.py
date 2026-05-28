class MockAIProvider:
    @staticmethod
    def generate_candidate_summary(candidate_data: dict) -> str:
        first_name = candidate_data.get("first_name", "Candidate")
        last_name = candidate_data.get("last_name", "")
        email = candidate_data.get("email", "")
        source = candidate_data.get("source", "Unknown")
        
        summary = f"""
        Professional Summary

        {first_name} {last_name} is a skilled professional who has applied through {source}.
        
        Contact: {email}
        
        Key Strengths:
        - Strong technical background with diverse experience
        - Problem-solving and analytical capabilities
        - Team collaboration and communication skills
        - Adaptability to new technologies and environments
        
        This candidate shows promise for growth in a dynamic team environment.
        Further evaluation through interviews is recommended to assess alignment with role requirements.
        """
        
        return summary.strip()
