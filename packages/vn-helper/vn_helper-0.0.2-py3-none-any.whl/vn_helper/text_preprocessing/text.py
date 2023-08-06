import re
import string
from flashtext import KeywordProcessor
import json
import regex
import re

replace_list = {
    'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
    'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
    'ả': 'ả', 'ố': 'ố', 'u´': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
    'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
    'ẻ': 'ẻ', 'àk': u' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á'}

standardwords = {'ok': ['ok', 'ô kêi', 'okie', 'o kê', 'okey', 'ôkê', 'okay', 'oki', 'oke', 'okê'], 'điện thoại thông minh': ['smp'], 'cảm ơn': ['cảm ơn', 'cám ơn', 'tks', 'thks', 'thanks', 'ths', 'thank you', 'thank u'], 'giống': ['giống', 'simili', 'similar', 'giốg'], 'không phải': ['kp'], 'làm sao': ['lsao'], 'thương mại điện tử': ['tmđt'], 'android': ['andoid', 'androi'], 'đéo': ['đéo', 'dél', 'éo'], 'dễ thương': ['cute', 'dễ thg', 'dthg'], 'với': ['vs', 'zới'], 'vậy': ['zỵ', 'zị', 'dẹ', 'dỵ', 'zậy'], 'được': ['đươc', 'đc', 'đk', 'dk', 'đx', 'dc'], 'quá': ['wa', 'wá', 'qá'], 'đường dẫn': ['link'], 'bhxh': ['bảo hiểm xã hội'], 'bhyt': ['bảo hiểm y tế'], 'bhtn': ['bảo hiểm thân thể'], 'kích cỡ': ['sz', 'size'], 'chuẩn chính hãng': ['authentic', 'auth'], 'xóa': ['delete', 'del'], 'thích': ['thick', 'thk', 'thich', 'thch', 'thik', 'like', 'thish'], 'tốt': ['good', 'god', 'gút', 'gut', 'tot', 'tôt', 'nice', 'gud', 'wel done'], 'rất tốt': ['perfect'], 'cửa hàng': ['store', 'shop', 'sop'], 'sản phẩm': ['sp', 'product'], 'chiết khấu': ['comision'], 'bình thường': ['bt', 'bthg', 'btg', 'bình thg', 'bình tg'], 'thời gian': ['time', 'tgian', 'thgian'], 'giao hàng': ['ship', 'síp', 'delivery'], 'xấu': ['sấu', 'xau'], 'mình': ['mik', 'mh', 'mih', 'mìh'], 'tôi cũng vậy': ['me too'], 'chất lượng': ['quality', 'chat lượng', 'chất lg'], 'hoàn hảo': ['excelent'], 'lỡ': ['nhỡ'], 'dùng': ['dùg'], 'apple': ['aple'], 'apple tv': ['apletv'], 'deathadder': ['deathader'], 'blackberry': ['blackbery'], 'tệ': ['bad', 'sad', 'por', 'poor'], 'hạn sử dụng': ['date', 'exp', 'expiry date', 'hsd'], 'đẹp': ['đep', 'dep'], 'trả lời': ['trã'], 'rồi': ['rồi', 'roài', 'rùi'], 'twitter': ['twiter'], 'sử dụng': ['sd', 'sử dg', 'sử dụg', 'sdụg'], 'điện thoại': ['đt', 'đth', 'đthoai'], 'winner': ['winer'], 'nhắn tin': ['nt', 'inbox', 'inbx', 'ib', 'ntin'], 'xài': ['sài'], 'có': ['coá'], 'bây giờ': ['bi h', 'bi giờ', 'bây h', 'bi jờ', 'bj', 'bjo'], 'facebook': ['fb', 'fbook', 'facebok'], 'ngon': ['delicious'], 'hàng': ['hàg'], 'ios': ['ió'], 'bluetooth': ['bluetooh', 'blutooth '], 'giả mạo': ['fake'], 'matebook': ['matebok'], 'yêu': ['love', 'iu', 'iêu'], 'chú trọng': ['grace', 'chú trọng', 'chú chọng', 'trú trọng', 'trú chọng'], 'anh em': ['ae'], 'miễn phí': ['free', 'fre'], 'đáng yêu': ['lovely', 'đáng iu', 'đáng iêu'], 'vui vẻ': ['zui zẻ'], 'tuyệt vời': ['toẹt vời', 'tuyệt zời', 'toẹt zời', 'great'], 'ghét': ['gét'], 'dễ': ['dể'], 'viettel': ['vietel'], 'food': ['fod'], 'bạn': ['pạn'], 'nissan': ['nisan'], 'google': ['gogle', 'gg'], 'cái': ['kái'], 'hình': ['hìh'], 'còn': ['kòn'], 'hiểu': ['hỉu'], 'vacuum': ['vacum'], 'nhu cầu': ['nhu kầu'], 'của': ['kủa'], 'qua': ['wa'], 'số điện thoại': ['sđt'], 'ecommerce': ['ecomerce'], 'mang': ['mag'], 'mọi người': ['mn'], 'gì': ['ji'], 'nhiêu': ['nhiu'], 'bao nhiêu': ['bn'], 'blueotooth': ['blueototh'], 'nhỉ': ['nhỷ'], 'hỏi': ['hủi'], 'nếu': ['nhếu'], 'ạ': ['ậ', 'ợ'], 'đăng ký': ['đăng kí', 'dký', 'dkí', 'đkí', 'đký'], 'nhưng': ['nhg', 'nhưg'], 'sinh viên': ['svien'], 'như thế nào': ['ntn'], 'tăng': ['tăg'], 'thì': ['thỳ'], 'chỉ': ['chĩ'], 'khi': ['khj'], 'luôn': ['lun'], 'đích': ['đíck', 'đík', 'djk'], 'thi': ['thj'], 'nó': ['nóa'], 'này': ['nỳ'], 'hôm': ['hum'], 'biết': ['bik', 'bít'], 'nhiều': ['nhìu'], 'quan trọng': ['qtrong'], 'macbook': ['macbok'], 'đếch': ['đếk'], 'phải': ['fải'], 'sim': ['sjm'], 'con': ['kon'], 'giờ': ['gjờ'], 'trước': ['trc'], 'nước': ['nc'], 'cũng': ['kũng', 'cũg', 'kũg'], 'mà': ['màk'], 'thôi': ['hoi', 'thoi'], 'ví dụ': ['vd'], 'ngu': ['stupic']}



class Text:
    def __init__(self, text):
        self.text = text
        self.to_string()
        self.lowercase()

    def to_string(self):
        self.text = str(self.text)

    def lowercase(self):
        self.text = self.text.lower()

    def load_stopwords(self):
        with open('/data/vietnamese-stopwords.txt', 'r') as f:
            self.stopwords = f.read().splitlines()
            
    def load_standardwords(self):
        with open('/data/standard_words.json') as f_in:
            self.standardwords = json.load(f_in)


    def normalize(self):
        self.punctuate()
        self.regex_normalize()
        return self.text

    def punctuate(self):
        for k, v in replace_list.items():
            self.text = self.text.replace(k, v)

    def regex_normalize(self):
        patterns = ['\[([^\]=]+)(?:=[^\]]+)?\].*?\[\/\\1\\n]', r'\b(?:(?:https?|ftp)://)?\w[\w-]*(?:\.[\w-]+)+\S*',
                    "[\(\[].*?[\)\]]"]
        for pattern in patterns:
            self.text = re.sub(pattern, '', self.text)
        # chuyen punctuation thành space
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        self.text = self.text.translate(translator)

        # remove nốt những ký tự thừa
        self.text = self.text.replace(u'"', u' ')
        self.text = self.text.replace(u'️', u'')
        self.text = self.text.replace('🏻', '')
        self.text = self.text.replace('\r', '')
        # Remove numbers
        self.text = re.sub(r'\d+', ' ', self.text)
        # Removing multiple spaces
        self.text = re.sub(r'\s+', ' ', self.text)
        keyword_processor = KeywordProcessor(case_sensitive = False)
        keyword_dict = {'không': ['hông', 'hem', 'kô', 'hok', 'ko', 'khong',
                                  'k0', 'khog', 'kg', 'khg', 'ko', 'khôg'],
                        'không ': ['k ', 'kh '], 'blackberry': ['bb']}
        keyword_processor.add_keywords_from_dict(keyword_dict)
        self.text = keyword_processor.replace_keywords(self.text)
        #Chuan hoa english words
        keyword_processor.add_keywords_from_dict(standardwords)
        self.text = keyword_processor.replace_keywords(self.text)
        self.text = re.sub(r'\s+', ' ', self.text)
        self.text = self.text.strip()

