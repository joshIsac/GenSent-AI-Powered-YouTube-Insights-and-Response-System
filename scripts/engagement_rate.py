def calculate_engagement_rate(subscriber_count, view_count, comment_count, like_count):
    """
    Calculate the engagement rate based on given metrics.

    Engagement Rate Formula: (Comments + Likes) / Views * 100 to get the percentage.
    """
    try:
        # Safely convert inputs to integers or default to 0 if conversion fails
        subscriber_count = int(subscriber_count) if str(subscriber_count).isdigit() else 0
        view_count = int(view_count) if str(view_count).isdigit() else 0
        comment_count = int(comment_count) if str(comment_count).isdigit() else 0
        like_count = int(like_count) if str(like_count).isdigit() else 0

        # Prevent divide by zero
        if view_count == 0:
            return 0.0

        # Calculate engagement rate as: (Likes + Comments) / Views * 100
        engagement_rate = ((like_count + comment_count) / view_count) * 100
        return round(engagement_rate, 2)

    except Exception as e:
        # Return a meaningful error message if something goes wrong
        return {"error": f"Error calculating engagement rate: {str(e)}"}
