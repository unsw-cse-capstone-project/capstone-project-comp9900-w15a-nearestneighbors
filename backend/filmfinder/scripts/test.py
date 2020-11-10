from movies.models import MovieFeatures
import pandas as pd
from django_pandas.io import read_frame

def run():
    df = read_frame(MovieFeatures.objects.all())
    print(df)