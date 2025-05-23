

def connectGithub(request):
    """
    Connects a user to their GitHub account.
    """
    # Get the access token from the request
    access_token = request.data.get('access_token')
    
    # Validate the access token
    if not access_token:
        return Response({'error': 'Access token is required.'}, status=400)
    
    # Use the access token to fetch user information from GitHub
    github_user_info = get_github_user_info(access_token)
    
    if not github_user_info:
        return Response({'error': 'Invalid access token.'}, status=400)
    
    # Get or create a user in your database based on the GitHub user information
    user, created = User.objects.get_or_create(
        username=github_user_info['login'],
        defaults={
            'email': github_user_info['email'],
            'first_name': github_user_info['name'],
        }
    )
    
    if created:
        # If the user was created, you might want to send a welcome email or perform other actions
        pass
    
    # Generate a JWT token for the user
    token = generate_jwt_token(user)
    
    return Response({'token': token}, status=200)
