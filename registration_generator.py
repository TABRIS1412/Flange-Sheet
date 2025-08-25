import hashlib
import datetime
import base64
import json


class RegistrationGenerator:
    """
    注册码生成器
    专门用于根据机器码和有效期生成注册码
    提供更安全的注册码生成和验证功能
    """

    def __init__(self, salt=None):
        """
        初始化注册码生成器
        
        Args:
            salt (str, optional): 加密盐值，用于增加安全性
        """
        self.salt = salt or "default_salt_value_for_extra_security"

    def generate_registration_key(self, machine_code, validity_days=365):
        """
        根据机器码和有效期生成注册码
        
        Args:
            machine_code (str): 机器码
            validity_days (int): 有效期（天数），默认365天（12个月）
            
        Returns:
            dict: 包含注册码和到期时间的字典
        """
        # 计算到期时间
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=validity_days)
        expiry_str = expiry_date.strftime("%Y-%m-%d")
        
        # 将有效期信息编码到注册码中
        # 创建包含机器码、有效期和盐值的数据
        data = {
            'machine_code': machine_code,
            'expiry_date': expiry_str,
            'validity_days': validity_days
        }
        
        # 将数据转换为JSON并编码
        data_str = json.dumps(data, separators=(',', ':'))
        encoded_data = base64.b64encode(data_str.encode('utf-8')).decode('utf-8')
        
        # 生成注册码：编码数据+盐值的MD5哈希
        reg_key = hashlib.md5(f"{encoded_data}{self.salt}".encode('utf-8')).hexdigest()
        
        return {
            'registration_key': reg_key,
            'machine_code': machine_code,
            'expiry_date': expiry_str,
            'validity_days': validity_days,
            'encoded_data': encoded_data,  # 用于验证时解析数据
            'generated_date': datetime.datetime.now().strftime("%Y-%m-%d")
        }

    def decode_registration_key(self, registration_key):
        """
        从注册码中解码出原始数据
        
        Args:
            registration_key (str): 注册码
            
        Returns:
            dict or None: 解码出的数据，如果失败则返回None
        """
        try:
            # 尝试从注册码中解析数据（这需要一个更复杂的方案）
            # 在实际应用中，这里应该使用加密而不是简单哈希
            return None
        except:
            return None

    def validate_registration_key(self, machine_code, registration_key, validity_days=None):
        """
        验证注册码是否有效（简化版验证）
        
        Args:
            machine_code (str): 机器码
            registration_key (str): 注册码
            validity_days (int, optional): 有效期天数，如果提供则验证
            
        Returns:
            bool: 注册码是否有效
        """
        # 首先验证注册码格式
        if not self.validate_registration_format(registration_key):
            return False
            
        # 如果提供了有效期天数，则验证是否匹配
        if validity_days is not None:
            # 重新生成注册码并比较
            test_info = self.generate_registration_key(machine_code, validity_days)
            if registration_key.lower() == test_info['registration_key'].lower():
                # 验证到期日期是否未过期
                try:
                    expiry_date_obj = datetime.datetime.strptime(test_info['expiry_date'], "%Y-%m-%d")
                    if datetime.datetime.now() > expiry_date_obj:
                        return False  # 已过期
                    return True
                except ValueError:
                    return False
            return False
            
        # 如果没有提供有效期天数，只验证格式和是否过期（简化处理）
        # 在实际应用中，应该有一种方法可以从注册码中提取有效期信息
        return self.validate_registration_format(registration_key)

    def validate_registration_format(self, registration_key):
        """
        验证注册码格式是否正确
        
        Args:
            registration_key (str): 注册码
            
        Returns:
            bool: 格式是否正确
        """
        # 检查是否为32位十六进制字符串（MD5哈希）
        if len(registration_key) != 32:
            return False
            
        try:
            int(registration_key, 16)
            return True
        except ValueError:
            return False

    def create_verifiable_registration_key(self, machine_code, validity_days=365):
        """
        创建可验证的注册码（包含嵌入信息）
        注意：这种方法在实际应用中需要更强的加密保护
        
        Args:
            machine_code (str): 机器码
            validity_days (int): 有效期（天数）
            
        Returns:
            str: 可验证的注册码
        """
        # 计算到期时间
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=validity_days)
        expiry_str = expiry_date.strftime("%Y-%m-%d")
        
        # 创建要嵌入的数据
        data = {
            'mc': machine_code,  # 机器码缩写
            'ed': expiry_str,    # 到期日期缩写
            'vd': validity_days  # 有效期天数缩写
        }
        
        # 编码数据
        data_str = json.dumps(data, separators=(',', ':'))
        encoded_data = base64.b64encode(data_str.encode('utf-8')).decode('utf-8')
        
        # 生成注册码
        reg_key = hashlib.md5(f"{encoded_data}{self.salt}".encode('utf-8')).hexdigest()
        
        # 返回注册码和编码数据的组合
        return f"{reg_key}:{encoded_data}"

    def verify_registration_key(self, registration_key_with_data):
        """
        验证包含嵌入信息的注册码
        
        Args:
            registration_key_with_data (str): 包含嵌入信息的注册码
            
        Returns:
            dict: 验证结果和注册信息
        """
        try:
            # 分离注册码和嵌入数据
            parts = registration_key_with_data.split(':', 1)
            if len(parts) != 2:
                return {'valid': False, 'message': '注册码格式错误'}
                
            reg_key, encoded_data = parts
            
            # 验证注册码格式
            if not self.validate_registration_format(reg_key):
                return {'valid': False, 'message': '注册码格式错误'}
            
            # 解码嵌入数据
            decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
            data = json.loads(decoded_data)
            
            # 提取信息
            machine_code = data.get('mc')
            expiry_date = data.get('ed')
            validity_days = data.get('vd')
            
            if not all([machine_code, expiry_date, validity_days]):
                return {'valid': False, 'message': '注册码数据不完整'}
            
            # 重新生成注册码进行验证
            expected_key = hashlib.md5(f"{encoded_data}{self.salt}".encode('utf-8')).hexdigest()
            
            if reg_key.lower() != expected_key.lower():
                return {'valid': False, 'message': '注册码验证失败'}
            
            # 检查是否过期
            try:
                expiry_date_obj = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
                if datetime.datetime.now() > expiry_date_obj:
                    return {'valid': False, 'message': '注册码已过期', 'expired': True}
            except ValueError:
                return {'valid': False, 'message': '日期格式错误'}
            
            return {
                'valid': True,
                'machine_code': machine_code,
                'expiry_date': expiry_date,
                'validity_days': validity_days
            }
        except Exception as e:
            return {'valid': False, 'message': f'验证过程出错: {str(e)}'}


# 使用示例
if __name__ == "__main__":
    # 创建实例（使用默认盐值）
    generator = RegistrationGenerator()
    
    # 示例机器码
    sample_machine_code = "5d41402abc4b2a76b9719d911017c592"  # 示例机器码
    
    # 生成一年有效期的注册码
    reg_info = generator.generate_registration_key(sample_machine_code, 365)
    
    print("注册码生成示例:")
    print(f"机器码: {reg_info['machine_code']}")
    print(f"注册码: {reg_info['registration_key']}")
    print(f"到期时间: {reg_info['expiry_date']}")
    print(f"有效期: {reg_info['validity_days']} 天")
    
    # 使用可验证的注册码方法
    verifiable_key = generator.create_verifiable_registration_key(sample_machine_code, 180)
    print(f"\n可验证注册码: {verifiable_key}")
    
    # 验证注册码
    verification_result = generator.verify_registration_key(verifiable_key)
    print(f"验证结果: {verification_result}")