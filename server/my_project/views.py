"""
This page contains the view functions for the polarisation parallelogram graph generator.

Functions:
home_view: Sends a response to be displayed on an empty homepage, primarily for testing purposes.
parallelogram_view: Receives a POST request from end user, generates graph ands sends it back for display in base64 form.


Author: Joey Cartwright
Date: 20-07-2024
"""

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import json
from django.http import JsonResponse, HttpResponse
from my_project.polpargraph import parallelogram
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return HttpResponse("Welcome to the home page!")


@csrf_exempt
def parallelogram_view(request):
    """
    Receives the POST request from React containing the variables specified by the end user, and uses those variables to generate the graph through the parallelogram() function. Finally, sends the
    graph back in base64 Json format to React to be displayed on the website:

    Parameters:
    request: The POST request

    Raises:
        ValueError: If a variable designed for parallelogram() is missing
        Exception: Receives and sends any other errors specified and found in parallelogram()
    
    """

    try:

        dic_reception = json.loads(request.body)
        print(dic_reception)
        group_var = dic_reception["groupVar"]
        group_1_value = dic_reception["group1Value"]
        group_2_value = dic_reception["group2Value"]
        question = dic_reception["question"]

        if not all([group_var, group_1_value, group_2_value, question]):
            raise ValueError("At least one field is missing")

        parallelogram(group_var, group_1_value, group_2_value, question)

        buffer = BytesIO()
        plt.savefig(buffer, format = 'png', dpi=150)
        buffer.seek(0)
        graph = base64.b64encode(buffer.read()).decode('utf-8')

        plt.clf()
        plt.close()
    
        return JsonResponse({'graph': graph})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = 500)
