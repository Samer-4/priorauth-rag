from src.policy_rag import chunk_policy


def test_chunks_respect_size_limit():
    text = (
        "COVERAGE CRITERIA\n"
        "Chronic Weight Management (Adult)\n"
        + "The patient must meet the coverage requirements.\n" * 100
    )

    chunks = chunk_policy(text)

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= 1500 for chunk in chunks)


def test_section_metadata():
    text = (
        "COVERAGE CRITERIA\n"
        "Chronic Weight Management (Adult)\n"
        "The patient must be at least 18 years old.\n"
    )

    chunks = chunk_policy(text)

    matching = [
        chunk for chunk in chunks
        if "The patient must be at least 18" in chunk.page_content
    ]

    assert matching
    assert matching[0].metadata["section"] == "COVERAGE CRITERIA"
    assert "Adult" in matching[0].metadata["indication"]


def test_separate_authorization_sections():
    text = (
        "COVERAGE CRITERIA\n"
        "Chronic Weight Management (Adult)\n"
        "Initial authorization requires BMI of 35.\n"
        "CONTINUATION OF THERAPY\n"
        "Chronic Weight Management (Adult)\n"
        "Continuation requires maintaining weight loss.\n"
    )

    chunks = chunk_policy(text)

    initial = [
        chunk for chunk in chunks
        if "Initial authorization requires" in chunk.page_content
    ]

    continuation = [
        chunk for chunk in chunks
        if "Continuation requires" in chunk.page_content
    ]

    assert initial
    assert continuation

    assert initial[0].metadata["section"] == "COVERAGE CRITERIA"
    assert continuation[0].metadata["section"] == "CONTINUATION OF THERAPY"


def test_roman_numeral_heading():
    text = (
        "III.\n"
        "Wegovy injection is covered as medically necessary.\n"
        "FDA-Approved Indications\n"
        "1. Weight Loss in an Adult with Overweight or Obesity.\n"
        "A) Initial Therapy. Approve when criteria are met.\n"
        "i. Patient is 18 years of age or older.\n"
        "ii. Patient meets the baseline BMI requirement.\n"
    )

    chunks = chunk_policy(text)

    matching = [
        chunk for chunk in chunks
        if "Patient is 18 years" in chunk.page_content
    ]

    assert matching
    assert matching[0].metadata["section"] == "III."
    assert "Wegovy" in matching[0].metadata["medication"]
    assert "Initial Therapy" in matching[0].metadata["pathway"]
