################################################################################################################

# EXTERNAL MODULES TO BE USED

################################################################################################################

from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'c1155c6a351e49eba15c00ce577b259e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class RegisterForm(FlaskForm):
    email = StringField("邮箱", validators=[InputRequired(), Email(message="无效的邮箱"), Length(max=50)], render_kw={"placeholder": "example@gmail.com"})
    username = StringField("用户名", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "用户名"})
    password = PasswordField("密码", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "********"})
    submit = SubmitField("注册")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("用户名已存在，请重新输入.")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("邮箱已存在，请重新输入.")


class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[InputRequired(), Length(max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("密码", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder":  "Password"})
    submit = SubmitField("登录")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
    
        flash("User does not exist, or invalid username or password.")
    return render_template('login.html', title="Login", form=form)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Shop")
def Shop():
    #df = pd.read_csv("猫咖-点评.csv")
    #list = df.to_dict('records')
    list=[{'Unnamed: 0': 0, '店铺名称': '猫不理·猫咪咖啡·布偶猫舍', '店铺星级（50=5星）': 45, '人均消费': '54.0', '所在区域': '海琴广场', '团购': '190元 四人撸猫套餐（十六岁以下不接待）'}, {'Unnamed: 0': 1, '店铺名称': '喵小院猫咖The Cat Coffee(五四广场店)', '店铺星级（50=5星）': 45, '人均消费': '36.0', '所在区域': '万象城', '团购': '39.9元 晚场17-21点单人撸猫套餐'}, {'Unnamed: 0': 2, '店铺名称': '春夏秋猫咖啡·猫咪主题咖啡馆', '店铺星级（50=5星）': 45, '人均消费': '34.0', '所在区域': '长江路沿线', '团购': '无'}, {'Unnamed: 0': 3, '店铺名称': '狗窝窝Gowow·羊驼·猫咖狗咖', '店铺星级（50=5星）': 45, '人均消费': '76.0', '所在区域': '万象城', '团购': '88元 1-3楼单人通票·撸狗·撸羊驼·撸鸭·撸猫'}, {'Unnamed: 0': 4, '店铺名称': '六月猫咖·英短猫舍', '店铺星级（50=5星）': 50, '人均消费': '43.0', '所在区域': '台东步行街', '团购': '39.9元 撸猫单人餐，提供免费WiFi'}, {'Unnamed: 0': 5, '店铺名称': '三月猫咖', '店铺星级（50=5星）': 45, '人均消费': '45.0', '所在区域': '新都心', '团购': '99元 双人套餐，包间免费'}, {'Unnamed: 0': 6, '店铺名称': 'Coffee Meow 米奥猫咖', '店铺星级（50=5星）': 40, '人均消费': '29.0', '所在区域': '正阳路', '团购': '19元 喵星人单人饮品，有赠品'}, {'Unnamed: 0': 7, '店铺名称': '柴圆滚滚猫咪咖啡', '店铺星级（50=5星）': 45, '人均消费': '40.0', '所在区域': '中央商务区', '团购': '39.9元 单人超值撸喵体验券'}, {'Unnamed: 0': 8, '店铺名称': '布偶猫咖(台东步行街店)', '店铺星级（50=5星）': 35, '人均消费': '25.0', '所在区域': '台东步行街', '团购': '36.9元 单人撸猫体验，包间免费'}, {'Unnamed: 0': 9, '店铺名称': 'Café de DARI 达芮.猫咖啡馆(新城吾悦店)', '店铺星级（50=5星）': 40, '人均消费': '52.0', '所在区域': '海上嘉年华', '团购': '无'}, {'Unnamed: 0': 10, '店铺名称': '一树喵生撸猫下午茶猫咖啡馆', '店铺星级（50=5星）': 40, '人均消费': '46.0', '所在区域': '维客广场', '团购': '68元 单人限定静享下午茶时光套餐'}, {'Unnamed: 0': 11, '店铺名称': '福至猫吉·海景猫咖', '店铺星级（50=5星）': 40, '人均消费': '33.0', '所在区域': '融创茂', '团购': '无'}, {'Unnamed: 0': 12, '店铺名称': '猫在云端•猫咪咖啡•布偶猫舍', '店铺星级（50=5星）': 30, '人均消费': '无', '所在区域': '丽达购物广场', '团购': '72.8元 双人撸猫套餐5选2'}, {'Unnamed: 0': 13, '店铺名称': '喵町物语·宅猫咖', '店铺星级（50=5星）': 45, '人均消费': '36.0', '所在区域': '湛山/太平角', '团购': '78元 双人撸猫体验'}, {'Unnamed: 0': 14, '店铺名称': '杨小喵猫咖', '店铺星级（50=5星）': 45, '人均消费': '31.0', '所在区域': '维客广场', '团购': '55元 双人人套餐，包间免费'}, {'Unnamed: 0': 15, '店铺名称': '柴岛日记·柴犬狗咖·猫咖·海景咖啡店', '店铺星级（50=5星）': 40, '人均消费': '44.0', '所在区域': '五四广场商圈', '团购': '128元 双人暖心撸猫撸狗'}, {'Unnamed: 0': 16, '店铺名称': 'Gowow狗窝窝·楼上有猫咖(五四广场店)', '店铺星级（50=5星）': 40, '人均消费': '69.0', '所在区域': '万象城', '团购': '无'}, {'Unnamed: 0': 17, '店铺名称': '妙喵屋猫咖', '店铺星级（50=5星）': 35, '人均消费': '29.0', '所在区域': '青岛路', '团购': '49.9元 撸猫双人套餐，提供免费WiFi'}, {'Unnamed: 0': 18, '店铺名称': '海边的猫和咖啡馆', '店铺星级（50=5星）': 45, '人均消费': '50.0', '所在区域': '湛山/太平角', '团购': '无'}, {'Unnamed: 0': 19, '店铺名称': '你和猫&猫咖', '店铺星级（50=5星）': 35, '人均消费': '43.0', '所在区域': '石老人海水浴场商圈', '团购': '[猫咖]71.9元 双人撸猫券'}, {'Unnamed: 0': 24, '店铺名称': '一只狗的猫咖馆·爬宠·阿拉斯加', '店铺星级（50=5星）': 40, '人均消费': '42.0', '所在区域': '中央商务区', '团购': '45.5元 单人撸猫撸狗·爬宠互动体验（谢绝16岁以下儿童）'}, {'Unnamed: 0': 25, '店铺名称': 'Sweet cat·星愿猫咖', '店铺星级（50=5星）': 35, '人均消费': '31.0', '所在区域': '长江路沿线', '团购': '25.8元 单人撸猫套餐，提供免费WiFi'}, {'Unnamed: 0': 26, '店铺名称': '小巫咖啡馆', '店铺星级（50=5星）': 45, '人均消费': '54.0', '所在区域': '湛山/太平角', '团购': '无'}, {'Unnamed: 0': 27, '店铺名称': '晴天猫星球·猫咪咖啡', '店铺星级（50=5星）': 45, '人均消费': '69.0', '所在区域': '新都心', '团购': '68.8元 暖冬单人餐❤，提供免费WiFi'}, {'Unnamed: 0': 28, '店铺名称': '朵猫猫撸猫咖啡馆', '店铺星级（50=5星）': 45, '人均消费': '44.0', '所在区域': '新都心', '团购': '49.9元 单人撸猫套餐（14周岁以下不接待）'}]
    return render_template('Shop.html', entries = list, encoding="utf-8")


@app.route("/Contact")
def Contact():
    return render_template('Contact.html')


@app.route("/Guide")
def Guide():
    return render_template('Guide.html')


################################################################################################################

# ERROR HANDLERS

################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


################################################################################################################

# APPLICATION TEST RUN AT PORT 9003

################################################################################################################

if __name__ == '__main__':
    app.run('localhost', 8896)