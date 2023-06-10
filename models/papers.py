from connection import db as database

papers_ref = database.collection('papers')

def get_all_papers():
    return papers_ref.stream()

def add_paper(paper):
    papers_ref.document(paper['name']).set(paper)

