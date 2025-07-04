from Helper.helpers import Helper


class ResponseHelper:

    def get_post_to_facebook_response(success_post_count, failed_post_count):
        message = ""
        if not success_post_count and not failed_post_count:
            message = "No pages were posted. Added pages or update acess token."
        
        if success_post_count:
            message += f"Successfully posted {success_post_count} pages. "
        
        if failed_post_count:
            message += f"Failed to post {failed_post_count} pages."

        response = {
            'status': True,
            'message': message,
            'success_post_count': success_post_count,
            'failed_post_count': failed_post_count,
        }
        return response
    
    def get_new_news_added_response(data):
        message = f"{len(data)} New news added! 🥺😔😭"
        if len(data):
            message = message[:-5] + " successfully 😍😎😜"

        response = {
            'status': True,
            'message': message,
        }
        return response
    
    def get_news_response(serializer):
        count, caches_data = Helper.get_all_page_cache()
        cache_response = {
            # 'status': True,
            # 'time': timezone.localtime(),
            'message': "Here's the latest news queue now!",
            'total_posts_count': count,
            # 'caches_data': caches_data,
        }
        response = {
            'status': True,
            'count': len(serializer.data),
            'response_duration': 0,
            'message': f"{len(serializer.data)} news fetched successfully.",
            'cache_response': cache_response,
            'data': serializer.data,
        }
        return response

