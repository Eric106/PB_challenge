from mysql.connector import connect, MySQLConnection
from mysql.connector.errors import IntegrityError, DatabaseError
from dataclasses import dataclass, field
from datetime import datetime
from pytz import utc
from decimal import Decimal
from uuid import uuid4
from .config import CONFIG
from .sql import Template

def get_conn() -> MySQLConnection:
    conn = None
    try:
        conn = connect(
            host=CONFIG.db_host,
            user=CONFIG.db_user,
            password=CONFIG.db_pass,
            database=CONFIG.db_schema
        )
    except DatabaseError as e:
        print(e)
    return conn

@dataclass(frozen=False)
class User:
    user_name: str = field(init=True,default=None)
    password: str = field(init=True,default=None)
    user_id: str = field(init=True,default=None)
    is_valid: bool = field(init=False)

    def create(self):
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor()
        try:
            self.user_id = str(uuid4())
            cursor.execute(Template.insert_user, params=(
                self.user_id,
                self.user_name,
                self.password,
                CONFIG.secret_key,
                datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            ))
            conn.commit()
            self.is_valid = True
        except IntegrityError:
            self.is_valid = False
        cursor.close()
        conn.close()

    def verify_login(self):
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(Template.get_user, params=(
            CONFIG.secret_key,
            self.user_name
        ))
        result : dict = cursor.fetchone()
        if result == None:
            self.is_valid = False
        else:
            self.is_valid = self.password == result['password']
            if self.is_valid:
                self.user_id = result['user_id']
        cursor.close()
        conn.close()

    def get_pb_points(self) -> Decimal:
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(Template.get_user_pb_points, params=(
            self.user_id,
        ))
        result : dict = cursor.fetchone()
        cursor.close()
        conn.close()
        if result != None:
            return result.get('pb_points')
        else:
            return None
        
    def get_investments(self) -> list[dict]:
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(Template.get_investments, params=[self.user_id])
        result : list[dict] = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def set_pb_points(self, pb_points):
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor()
        cursor.execute(Template.update_user_pb_points, params=(
            pb_points,
            self.user_id,
        ))
        conn.commit()
        cursor.close()
        conn.close()


@dataclass(frozen=False)
class Investment:
    investment_id: str = field(init=True, default='')
    user_id: str = field(init=True, default='')
    total_investment: Decimal = field(init=True, default=Decimal(0.0))
    pb_points: Decimal = field(init=True, default=Decimal(0.0))
    pay_method: str = field(init=True, default='')
    pb_commission_rate: Decimal = field(init=True, default=Decimal(0.05))
    pb_commission: Decimal = field(init=False)
    iva_pb_commission_rate: Decimal = field(init=True, default=Decimal(0.16))
    iva_pb_commission: Decimal = field(init=False)
    var_pay_commission_rate : Decimal = field(init=True, default=Decimal(0.024))
    var_pay_commission : Decimal = field(init=False)
    iva_var_pay_commission_rate : Decimal = field(init=True, default=Decimal(0.16))
    iva_var_pay_commission: Decimal = field(init=False)
    total_to_pay : Decimal = field(init=False)
    date_last_update: datetime = field(init=False)

    def __post_init__(self):
        self.calculator()
    
    def calculator(self):
        '''
        x = total_to_pay_VISA/MC,
        a = total_to_pay_SPEI,
        b = var_pay_commission_rate,
        c = iva_var_pay_commission_rate

            x = a + x(b) + (x(b))c ;
            x = a / (1-b-bc) ; 
        '''
        self.pb_commission = self.total_investment * self.pb_commission_rate
        self.iva_pb_commission = self.pb_commission * self.iva_pb_commission_rate
        self.total_to_pay = (self.total_investment - self.pb_points) + \
            self.pb_commission + self.iva_pb_commission
        if self.pay_method == 'VISA/MC':
            var_pay_comm_and_iva = 1 - self.var_pay_commission_rate - \
                (self.var_pay_commission_rate * self.iva_var_pay_commission_rate)
            self.total_to_pay = self.total_to_pay / var_pay_comm_and_iva
            self.var_pay_commission = self.total_to_pay * self.var_pay_commission_rate
            self.iva_var_pay_commission = self.var_pay_commission * self.iva_pb_commission_rate
        elif self.pay_method == 'SPEI':
            self.var_pay_commission = Decimal(0)
            self.iva_var_pay_commission = Decimal(0)

    def set_all_null(self):
        for col in self.to_dict().keys():
            self.__setattr__(col, None)
          
    def is_null(self) -> bool:
        return all(value==None for value in self.to_dict().values())

    def to_dict(self) -> dict:
        data : dict = self.__dict__
        for col in data.keys():
            value = data[col]
            if isinstance(value, Decimal):
                decimals = 4 if '_rate' in col else 2
                value = float(round(value, decimals))
            data[col] = value
        return data

    
    def from_dict(self, data:dict):
        try:
            for col in data.keys():
                value = data[col]
                if isinstance(value, float) or isinstance(value, str):
                    try:
                        value = Decimal(value)
                    except Exception:
                        pass
                self.__setattr__(col, value)
        except Exception:
            self.set_all_null()

    def create(self):
        user = User(user_id=self.user_id)
        user_pb_points = user.get_pb_points()
        if user_pb_points != None:
            user_pb_points = user_pb_points - self.pb_points
            if user_pb_points < Decimal(0):
                self.set_all_null()
                return
            else:
                user.set_pb_points(user_pb_points)
        self.date_last_update = datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor()
        try:
            self.investment_id = str(uuid4())
            cursor.execute(Template.insert_investment, params=(
                self.investment_id, self.user_id, self.date_last_update,
                self.total_investment, self.pb_points, self.pay_method,
                self.pb_commission_rate, self.pb_commission,
                self.iva_pb_commission_rate, self.iva_pb_commission, 
                self.var_pay_commission_rate, self.var_pay_commission, 
                self.iva_var_pay_commission_rate, self.iva_var_pay_commission,
                self.total_to_pay
            ))
            conn.commit()
        except IntegrityError as e:
            print(f'ERROR at insert investment: {self.to_dict()}',e)
        cursor.close()
        conn.close()  
    
    def get(self):
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(Template.get_investment, params=(
            self.investment_id,
            self.user_id
        ))
        result : dict = cursor.fetchone()
        if result == None:
            self.set_all_null()
        else:
            for col, value in result.items():
                self.__setattr__(col, value)
        cursor.close()
        conn.close()

    def update(self, data: dict):
        self.total_investment = Decimal(data.get('total_investment'))
        self.pb_points = Decimal(data.get('pb_points'))
        self.pay_method = data.get('pay_method')
        self.date_last_update = datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.calculator()
        
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(Template.update_investment, params=(
                self.date_last_update,
                self.total_investment, self.pb_points, self.pay_method,
                self.pb_commission_rate, self.pb_commission,
                self.iva_pb_commission_rate, self.iva_pb_commission, 
                self.var_pay_commission_rate, self.var_pay_commission, 
                self.iva_var_pay_commission_rate, self.iva_var_pay_commission,
                self.total_to_pay,
                self.investment_id, self.user_id
            ))
            conn.commit()
        except IntegrityError as e:
            print(f'ERROR at update investment: {self.to_dict()}',e)
        cursor.close()
        conn.close()

    def delete(self):
        conn : MySQLConnection = get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(Template.delete_investment, params=(
                self.investment_id, self.user_id
            ))
            conn.commit()
        except IntegrityError as e:
            print(f'ERROR at delete investment: {self.to_dict()}',e)
        cursor.close()
        conn.close()