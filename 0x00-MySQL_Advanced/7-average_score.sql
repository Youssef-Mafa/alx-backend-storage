-- stored procedure ComputeAverageScoreForUser that computes and 
--                      store the average score for a student. Note: An average score can be a decimal


DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    UPDATE users 
    SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = p_user_id)
    WHERE id = p_user_id;
END //
DELIMITER ;

