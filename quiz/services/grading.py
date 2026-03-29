def calculate_quiz_score(quiz, answers_list):
    questions = quiz.get_questions() 
    
    if questions is None:
        return {"error": "Неизвестный тип квиза"}
        
    total_questions = questions.count()
    if total_questions == 0:
        return {"error": "В квизе нет вопросов"}

    user_answers = {str(item.get('question_id')): item.get('answer') for item in answers_list}
    quiz_type_name = quiz.quiz_type.name.strip().lower().replace("_", " ")
    
    results = []
    correct_count = 0
    question_dict = {str(q.id): q for q in questions}

    for q_id, question in question_dict.items():
        user_answer = user_answers.get(q_id) 
        
        if quiz_type_name == 'async sorter':
            correct_answer = question.correct_sequence
            is_correct = (user_answer == correct_answer)
            
        elif quiz_type_name == 'true false':
            correct_answer = question.correct_answer
            is_correct = (str(user_answer).lower() == str(correct_answer).lower()) if user_answer is not None else False

        elif quiz_type_name == 'code ordering':
            lines = question.code_lines
            sorted_lines = sorted(lines, key=lambda x: x.get('correctPosition', 0))
            correct_answer = [line['id'] for line in sorted_lines]
            is_correct = (user_answer == correct_answer) if isinstance(user_answer, list) else False
            
        else:
            correct_answer = question.correct_answer
            is_correct = (str(user_answer).strip().lower() == str(correct_answer).strip().lower()) if user_answer is not None else False

        if is_correct:
            correct_count += 1
            
        results.append({
            "question_id": int(q_id),
            "is_correct": is_correct,
            "user_answer": user_answer
        })

    score = (correct_count / total_questions) * 100

    return {
        "score": score,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "results": results
    }