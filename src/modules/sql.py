

class Template:
    
    get_user = '''
SELECT user_id, user_name,
    CAST(AES_DECRYPT(password, SHA2(%s, 512)) AS CHAR(50)) as password,
    date_last_update, pb_points
FROM user
WHERE user_name = %s ;
'''

    get_user_pb_points = '''
SELECT user_id, pb_points
FROM user
WHERE user_id = %s ;
'''

    insert_user = '''
INSERT INTO user (user_id, user_name, password, date_last_update)
VALUES (%s, %s, AES_ENCRYPT(%s,SHA2(%s,512)), %s );
'''

    update_user_pb_points = '''
UPDATE user SET pb_points = %s
WHERE user_id = %s ;
'''

    insert_investment = '''
INSERT INTO investment (investment_id, user_id, date_last_update,
    total_investment, pb_points, pay_method,
    pb_commission_rate, pb_commission,
    iva_pb_commission_rate, iva_pb_commission,
    var_pay_commission_rate, var_pay_commission,
    iva_var_pay_commission_rate, iva_var_pay_commission, 
    total_to_pay)
VALUES (%s, %s, %s,
    %s, %s, %s,
    %s, %s, 
    %s, %s,
    %s, %s,
    %s, %s,
    %s);
'''

    get_investment = '''
SELECT investment_id, user_id, date_last_update,
    total_investment, pb_points, pay_method,
    pb_commission_rate, pb_commission,
    iva_pb_commission_rate, iva_pb_commission,
    var_pay_commission_rate, var_pay_commission,
    iva_var_pay_commission_rate, iva_var_pay_commission, 
    total_to_pay
FROM investment
WHERE investment_id = %s and user_id = %s ;
'''

    get_investments = '''
SELECT investment_id, user_id, date_last_update,
    total_investment, pb_points, pay_method,
    pb_commission_rate, pb_commission,
    iva_pb_commission_rate, iva_pb_commission,
    var_pay_commission_rate, var_pay_commission,
    iva_var_pay_commission_rate, iva_var_pay_commission, 
    total_to_pay
FROM investment
WHERE user_id = %s ;
'''

    update_investment = '''
UPDATE investment SET date_last_update = %s,
    total_investment = %s, pb_points = %s, pay_method = %s,
    pb_commission_rate = %s, pb_commission = %s,
    iva_pb_commission_rate = %s, iva_pb_commission = %s,
    var_pay_commission_rate = %s, var_pay_commission = %s,
    iva_var_pay_commission_rate = %s, iva_var_pay_commission = %s,
    total_to_pay = %s
WHERE investment_id = %s and user_id = %s ;
'''

    delete_investment = '''
DELETE FROM investment
WHERE investment_id = %s and user_id = %s ;
'''
