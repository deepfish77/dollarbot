import boto3

session = boto3.resource("dynamodb")


def get_question(question):

    table = session.Table("follow_up_questions")
    returned_question = table.get_item(Key={"question": question})
    print("question", returned_question)
    return returned_question


# get_user("deepfish+123@gmail.com")


def add_follow_up_review_question(
    category, question, feature_name, table_name="follow_up_questions"
):
    table = session.Table(table_name)
    table.put_item(
        Item={
            "category": category,
            "question": question,
            "feature_name": feature_name,
        }
    )

