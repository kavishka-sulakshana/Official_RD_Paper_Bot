def generate_marks_message(ptype="ONLINE", year="2023", paper_no="23", name="Kavishka Sulakshana", marks="80",
                           Drank="20", Arank="40", link="http//:abc.com"):
    message = f"""
        🛑 {year} PAPER {paper_no} ({ptype}) 📝
        ————————————————

        😀 Your Name : {name}

        💡 Your Marks : {marks} %

        🏅 Rank : {Drank} 

        ————————————————
    """

    return message


def generate_analytics_message(paperCount, average, markList: dict, className):
    message = f"""
        📊 <u>ANALYTICS OF {className}</u> \n
        📝 Total Papers Done : <b>{paperCount}</b> 
        🔥 Average Marks : <b>{average}%</b>
        ___________________________________\n
        👇🏼  <i>Your Mark List :</i> 
    """
    for key in markList:
        if markList[key] is None:
            message += f"""
            💎 Paper {key} : <b>Not Done</b>
        """
        else:
            message += f"""
                💎 Paper {key} : <b>{markList[key]}%</b>
            """
    return message
