import json
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
from ml_model import MLAnalysis


def save_analysis_to_db(company_id, pros_cons):
    """
    Saves or updates Pros & Cons ML analysis results for a single company.
    """

    session = SessionLocal()

    try:
        existing = (
            session.query(MLAnalysis)
            .filter_by(company_id=company_id)
            .first()
        )

        pros_json = json.dumps(pros_cons.get("top_pros", []), indent=4)
        cons_json = json.dumps(pros_cons.get("top_cons", []), indent=4)

        if existing:
            # UPDATE
            existing.pros = pros_json
            existing.cons = cons_json
            existing.updated_at = datetime.utcnow()
            print(f"🔁 Updated ML analysis for {company_id}")

        else:
            # INSERT NEW
            new_entry = MLAnalysis(
                company_id=company_id,
                pros=pros_json,
                cons=cons_json,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(new_entry)
            print(f"🆕 Inserted ML analysis for {company_id}")

        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ SQLAlchemy Error for {company_id}: {e}")

    finally:
        session.close()



def save_batch_analysis(all_results: dict):
    """
    Saves ML pros & cons for ALL companies in a batch pipeline.
    Called inside main_fin_analysis.py
    """
    print("\n📦 Saving ML analysis for all companies...")

    for company_id, pros_cons in all_results.items():
        save_analysis_to_db(company_id, pros_cons)

    print("✅ All ML analysis saved successfully.")
