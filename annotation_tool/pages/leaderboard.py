from datetime import date, timedelta

import pandas as pd
import streamlit as st

from annotation_tool.backend.config import get_competition_date
from annotation_tool.backend.models import get_leaderboard_counts

ANNOTATION_SCORE_FACTOR = 5
EVALUATION_SCORE_FACTOR = 1

competition_start_date = get_competition_date("competition_start_date") or date(2022, 11, 23)
competition_end_date = get_competition_date("competition_end_date") or date(2023, 1, 31)
prize_claim_date = competition_end_date + timedelta(weeks=4)


def show():
    st.header("📊 Leaderboard")

    st.dataframe(get_leaderboard_dataframe(), use_container_width=True)

    prize_info = f"""
    ### Competition 🏆

    If you contribute to Song Describer, you'll also have a chance to win one of our prizes!

    As a way to say thank you for your time and effort, we will send you a music-related gift 
    voucher of your choice (e.g. for music stores, streaming platforms, online music magazines, etc.) 
    if you are among the 3 users with the highest overall score during the competition period:

    * 🥇 1st place: £50
    * 🥈 2nd place: £30
    * 🥉 3rd place: £10 

    The competition opens on {competition_start_date:%d/%m/%Y} and ends on {competition_end_date:%d/%m/%Y} GMT.

    #### How do I enter the competition?
    All users contributing to Song Describer while the competition is running will automatically be considered
    participants. 
    
    #### How are contributions evaluated?
    You will be awarded points every time you complete an annotation or evaluation. 
    The overall contribution score is computed as follows:
    * 5 points for every annotation
    * 1 point for every evaluation

    If you'd like to save your progress and come back to Song Describer later on, you can log back onto 
    your profile by providing your unique user ID. If you're unable to provide your user ID, you will 
    not be able to recover your profile and you'll lose your progress.

    If you'd like to publicly track your progress on the leaderboard, you can also choose a nickname
    when you create your profile. 

    #### How do I claim my prize?
    If you're one of the top 3 ranked contributors on our leaderboard when the competition ends, you 
    can claim your prize by emailing your unique user ID to [i.manco@qmul.ac.uk](mailto:i.manco@qmul.ac.uk) 
    by {prize_claim_date:%d/%m/%Y}. Please note, if you cannot provide your user ID, we will not be able to verify your
    contributions and you won't be able to claim your prize.

    We will check that your contributions adhere to the annotation guidelines outlined on this platform
    and we reserve the right to refuse to award the prize if we find, at our sole discretion, that the 
    guidelines were not followed.
    """

    st.write(prize_info)


def get_leaderboard_dataframe():
    data = get_leaderboard_counts(competition_start_date, competition_end_date)
    captions_written_column = "Annotations"
    captions_evaluated_column = "Evaluations"
    name_column = "Nickname"
    score_column = "Score"
    df = pd.DataFrame(
        data,
        columns=[name_column, captions_written_column, captions_evaluated_column],
    )
    df[score_column] = (
        ANNOTATION_SCORE_FACTOR * df[captions_written_column]
        + EVALUATION_SCORE_FACTOR * df[captions_evaluated_column]
    )
    df[name_column] = df[name_column].fillna("Anonymous user")
    sorted_df = df.sort_values(score_column, ascending=False, ignore_index=True)
    sorted_df.index += 1  # index start at 1 not zero for nicer leaderboard
    return sorted_df


if __name__ == "__main__":
    show()
