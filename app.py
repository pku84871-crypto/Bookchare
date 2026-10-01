from datetime import date, timedelta
import base64
import streamlit as st

# ==============================================================================
# 1. Page Configuration & Custom Styling
# ==============================================================================
st.set_page_config(
    page_title="BookShare - ร้านหนังสือ & เช่ายืมออนไลน์",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Mali:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Kanit', sans-serif !important;
        background-color: #F8F3EC !important;
        color: #382B24 !important;
    }

    h1, h2, h3, .font-cute {
        font-family: 'Mali', cursive !important;
        color: #4A3528 !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1240px !important;
    }

    /* Badges */
    .badge-available {
        background-color: #588157;
        color: #FFFFFF;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-rented {
        background-color: #D9534F;
        color: #FFFFFF;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-sale {
        background-color: #BC6C25;
        color: #FFFFFF;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-mybook {
        background-color: #7251B5;
        color: #FFFFFF;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-condition {
        background-color: #FFFFFF;
        color: #4A3528;
        border: 1px solid #EADBCE;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 600;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #F3E9DD 0%, #EFE1D1 100%);
        border-radius: 24px;
        padding: 32px 36px;
        border: 1px solid #E5D7C7;
        margin-bottom: 24px;
    }
    .hero-badge {
        display: inline-block;
        background-color: #DCE8DA;
        color: #385E38;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .hero-h1 {
        font-family: 'Mali', cursive !important;
        font-size: 34px;
        font-weight: 700;
        color: #4A3528;
        line-height: 1.25;
        margin-bottom: 12px;
    }
    .hero-desc {
        font-size: 14px;
        color: #6C5E53;
        line-height: 1.6;
        margin-bottom: 20px;
        max-width: 580px;
    }

    /* Book Cards */
    .card-book {
        background-color: #FFFFFF;
        border: 1px solid #EADBCE;
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(61,46,36,0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .book-cover-img {
        width: 100%;
        aspect-ratio: 3/4;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #4A3528 !important;
        color: #FAF5EF !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        font-family: 'Kanit', sans-serif !important;
        transition: all 0.2s !important;
    }
    .stButton>button:hover {
        background-color: #BC6C25 !important;
        color: #FFFFFF !important;
    }

    .btn-cart-rent>button {
        background-color: #EAF2E8 !important;
        color: #2F5930 !important;
        border: 1px solid #C0DAC0 !important;
        border-radius: 999px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }
    .btn-cart-buy>button {
        background-color: #FAEEE1 !important;
        color: #9C5212 !important;
        border: 1px solid #EAC8A8 !important;
        border-radius: 999px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #DACABD !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. Complete Initial Mock Data
# ==============================================================================
MOCK_BOOKS = [
    {
        'id': 1,
        'title': 'Atomic Habits (ฉบับแปลไทย)',
        'full_title': 'Atomic Habits: เพราะชีวิตดีได้กว่าที่เป็น',
        'author': 'James Clear (แปลโดย ประภากาศ บริบูรณ์พาณิชย์)',
        'category': 'จิตวิทยา & พัฒนาตนเอง',
        'isbn': '978-616-287-343-0',
        'status': 'available',
        'status_text': '🟢 พร้อมให้ยืม',
        'condition': 'สภาพ 95%',
        'condition_full': 'สภาพดีเยี่ยม 95%',
        'buy_price': 280,
        'original_price': 330,
        'rent_price': 7,
        'deposit': 150,
        'img': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80',
        'desc': 'หนังสือระดับโลกที่จะเปลี่ยนความคิดและพฤติกรรมทีละ 1% เพื่อสร้างผลลัพธ์มหาศาล เหมาะอย่างยิ่งสำหรับผู้ที่ต้องการปลดล็อกศักยภาพในทุกๆ วัน',
        'seller_name': 'ร้านคุณมัสยิดนักอ่าน',
        'seller_rating': 4.9,
        'seller_count': 142,
        'is_my_book': False
    },
    {
        'id': 2,
        'title': 'ปาฏิหาริย์ร้านชำของคุณนามิยะ',
        'full_title': 'ปาฏิหาริย์ร้านชำของคุณนามิยะ (Miracles of the Namiya General Store)',
        'author': 'ฮิงาชิโนะ เคโงะ',
        'category': 'วรรณกรรม & นิยายแปล',
        'isbn': '978-616-18-2234-7',
        'status': 'rented',
        'status_text': '🔴 ถูกยืมอยู่ (รอคิว 2 คน)',
        'available_date': 'ว่าง 28 ต.ค.',
        'condition': 'สภาพ 92%',
        'condition_full': 'สภาพดี 92%',
        'buy_price': 245,
        'original_price': 295,
        'rent_price': 6,
        'deposit': 120,
        'img': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80',
        'desc': 'เมื่อหัวขโมยสามคนหลบหนีไปซ่อนตัวในร้านชำร้างแห่งหนึ่ง แต่กลับได้รับจดหมายขอคำปรึกษาจากคนในอดีต เรื่องราวอบอุ่นหัวใจจึงเริ่มต้นขึ้น',
        'seller_name': 'ร้านวรรณกรรมอุ่นใจ',
        'seller_rating': 4.9,
        'seller_count': 98,
        'is_my_book': False
    },
    {
        'id': 3,
        'title': 'The Psychology of Money',
        'full_title': 'The Psychology of Money: จิตวิทยาว่าด้วยเงิน',
        'author': 'Morgan Housel',
        'category': 'ธุรกิจ & การลงทุน',
        'isbn': '978-616-8187-25-8',
        'status': 'sale_only',
        'status_text': '🏷️ สำหรับขายเท่านั้น',
        'condition': 'สภาพ 98% เหมือนใหม่',
        'condition_full': 'สภาพ 98% เหมือนใหม่ (เกือบมือหนึ่ง)',
        'buy_price': 230,
        'original_price': 290,
        'rent_price': 0,
        'deposit': 0,
        'img': 'https://images.unsplash.com/photo-1592496431122-2349e0fbc666?auto=format&fit=crop&w=600&q=80',
        'desc': 'ข้อคิดเรื่องเงิน อิสรภาพ และโชคลาภ ผ่าน 19 เรื่องสั้นที่สะท้อนว่าทัศนคติเกี่ยวกับเงินมีความสำคัญและส่งผลต่อชีวิตมากกว่าความรู้ทางคณิตศาสตร์',
        'seller_name': 'Wealth Books',
        'seller_rating': 5.0,
        'seller_count': 215,
        'is_my_book': False
    },
    {
        'id': 4,
        'title': 'คิดแบบยิว ทำแบบญี่ปุ่น',
        'full_title': 'คิดแบบยิว ทำแบบญี่ปุ่น (Jewish Mind Japanese Execution)',
        'author': 'ฮอนดะ เคน',
        'category': 'ธุรกิจ & การลงทุน',
        'isbn': '978-616-287-112-2',
        'status': 'available',
        'status_text': '🟢 พร้อมให้ยืม',
        'condition': 'สภาพ 90%',
        'condition_full': 'สภาพ 90% สมบูรณ์',
        'buy_price': 190,
        'original_price': 250,
        'rent_price': 5,
        'deposit': 100,
        'img': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&w=600&q=80',
        'desc': 'บทเรียนชีวิตและธุรกิจจากมหาเศรษฐีชาวยิว ถ่ายทอดผ่านความมุ่งมั่นสไตล์คนญี่ปุ่น นำไปประยุกต์ใช้เพื่อความมั่งคั่งที่ยั่งยืน',
        'seller_name': 'BookHouse สยาม',
        'seller_rating': 4.8,
        'seller_count': 87,
        'is_my_book': False
    }
]

# ==============================================================================
# 3. Session State Initialization
# ==============================================================================
if 'all_books' not in st.session_state:
    st.session_state.all_books = MOCK_BOOKS.copy()

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'

if 'seller_subview' not in st.session_state:
    st.session_state.seller_subview = 'shelf'  # 'shelf' or 'add_book'
    
if 'edit_book_id' not in st.session_state:
    st.session_state.edit_book_id = None

if 'shelf_books' not in st.session_state:
    st.session_state.shelf_books = [
        {
            'id': 101,
            'title': 'กล้าที่จะถูกเกลียด (Courage to be Disliked)',
            'author': 'โดย คิชิมิ อิชิโร และ โคะกะ ฟุมิทะเกะ',
            'category': 'หมวดจิตวิทยา & ความสุข',
            'year': 'พิมพ์ปี 2023',
            'img': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80',
            'status': 'rented',
            'borrower_name': 'คุณกานต์ ว.',
            'days_left': 'เหลือ 4 วัน (คืน 28 ก.พ.)',
            'shipping': 'ส่งเคอรี่',
            'cond1': 'สภาพ 95% เหมือนใหม่',
            'cond2': 'ไม่มีไฮไลต์',
            'rate_label': 'ค่าเช่ารายสัปดาห์',
            'rate_val': '฿35 / 7 วัน',
            'income_label': 'ทำเงินสะสมแล้ว',
            'income_val': '฿420 (ยืม 12 ครั้ง)',
            'btn1': '📖 ประวัติยืม',
            'btn2': '✏️ แก้ไขเล่ม'
        },
        {
            'id': 102,
            'title': 'Atomic Habits เพราะชีวิตดีได้กว่าที่เป็น',
            'author': 'โดย James Clear (แปลโดย ประภาสิณี)',
            'category': 'การบริหารเวลา & นิสัย',
            'year': 'พิมพ์ปี 2022',
            'img': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=600&q=80',
            'status': 'avail_rent_sale',
            'cond1': 'สภาพ 90%',
            'cond2': 'ห่อปกพลาสติกใส',
            'rate_label': 'เช่า ฿7/วัน (฿42/wk)',
            'rate_val': 'หรือขายขาด ฿240',
            'income_label': 'ทำเงินสะสมแล้ว',
            'income_val': '฿315 (ยืม 5 ครั้ง)',
            'btn1': '👁️ สถานะเปิดอยู่',
            'btn2': '⚙️ ปรับราคา'
        },
        {
            'id': 103,
            'title': 'ด้วยรัก ความตาย และหัวใจสลาย',
            'author': 'โดย ฮารูกิ มูราคามิ (แปลโดย นพดล เวชสวัสดิ์)',
            'category': 'วรรณกรรมแปลคลาสสิก',
            'year': 'ฉบับสะสมปกแข็ง',
            'img': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80',
            'status': 'private',
            'review_rating': '★ 5.0 (รีวิวของฉัน)',
            'cond1': 'สภาพ 98% สะสม',
            'cond2': 'มีลายเซ็นผู้แปล',
            'rate_label': 'สถานะบนชั้น',
            'rate_val': 'เก็บไว้อ่านเอง',
            'income_label': 'อ่านจบเมื่อ',
            'income_val': '14 ม.ค. 2026',
            'btn1': '📖 เปิดปล่อยเช่า',
            'btn2': '✍️ บันทึกอ่าน'
        },
        {
            'id': 104,
            'title': 'จิตวิทยาว่าด้วยเงิน (Psychology of Money)',
            'author': 'โดย Morgan Housel',
            'category': 'การเงิน & ความมั่งคั่ง',
            'year': 'พิมพ์ปี 2021',
            'img': 'https://images.unsplash.com/photo-1592496431122-2349e0fbc666?auto=format&fit=crop&w=600&q=80',
            'status': 'avail_rent',
            'cond1': 'สภาพ 88% สภาพดี',
            'cond2': 'สันกระดาษสะอาด',
            'rate_label': 'อัตราให้เช่า',
            'rate_val': '฿8 / วัน (฿50/wk)',
            'income_label': 'ทำเงินสะสมแล้ว',
            'income_val': '฿590 (คืนทุนแล้ว)',
            'btn1': '🕒 ประวัติ 8 ครั้ง',
            'btn2': '✏️ แก้ไขเล่ม'
        }
    ]

if 'selected_book_id' not in st.session_state:
    st.session_state.selected_book_id = 1

if 'active_category' not in st.session_state:
    st.session_state.active_category = 'ทั้งหมด'

if 'search_query' not in st.session_state:
    st.session_state.search_query = ''

if 'form_key_suffix' not in st.session_state:
    st.session_state.form_key_suffix = 0

if 'user' not in st.session_state:
    st.session_state.user = {
        'logged_in': True,
        'name': 'คุณมีนา',
        'phone': '081-234-5678',
        'address': '123/45 ถนนมิตรภาพ แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร 10110',
        'tier': 'ผู้อ่านระดับ 2 (เช่าอยู่ 2 เล่ม)',
    }

if 'cart_rent' not in st.session_state:
    st.session_state.cart_rent = []

if 'cart_buy' not in st.session_state:
    st.session_state.cart_buy = []

if 'promo_code' not in st.session_state:
    st.session_state.promo_code = 'WELCOMEREAD'

if 'rental_days_choice' not in st.session_state:
    st.session_state.rental_days_choice = 10

if 'last_order' not in st.session_state:
    st.session_state.last_order = None

def get_book(book_id):
    for b in st.session_state.all_books:
        if b['id'] == book_id:
            return b
    return st.session_state.all_books[0]

def reset_add_book_form():
    st.session_state.form_key_suffix += 1

# ==============================================================================
# 4. Modals (Dialogs)
# ==============================================================================
@st.dialog("🔑 เข้าสู่ระบบ / สมัครสมาชิก")
def login_dialog():
    st.write("กรุณากรอกข้อมูลเพื่อเข้าสู่ระบบ BookShare")
    u_name = st.text_input("ชื่อ-นามสกุล", value=st.session_state.user.get('name', 'คุณมีนา'))
    u_phone = st.text_input("เบอร์โทรศัพท์", value=st.session_state.user.get('phone', '081-234-5678'))
    u_addr = st.text_area("ที่อยู่จัดส่ง", value=st.session_state.user.get('address', ''))

    if st.button("ตกลง / เข้าสู่ระบบ", use_container_width=True):
        if u_name and u_phone:
            st.session_state.user['logged_in'] = True
            st.session_state.user['name'] = u_name
            st.session_state.user['phone'] = u_phone
            st.session_state.user['address'] = u_addr
            st.success(f"ยินดีต้อนรับ {u_name} เข้าสู่ระบบแล้ว!")
            st.rerun()
        else:
            st.error("กรุณากรอกชื่อและเบอร์โทรศัพท์")

@st.dialog("📖 วิธีการยืม - คืนหนังสือ")
def how_it_works_dialog():
    st.markdown(
        """
        <div style="font-size:13px; line-height:1.7;">
            <b>1. เลือกหนังสือและระยะเวลา:</b> เลือกวันเริ่มและวันคืน (สูงสุด 30 วัน) ชำระค่ายืมและมัดจำ<br>
            <b>2. จัดส่งถึงบ้าน:</b> หนังสือผ่านการทำความสะอาดและอบฆ่าเชื้อ UV พร้อมส่งมอบ<br>
            <b>3. ส่งคืนสะดวก & รับมัดจำคืนทันที:</b> ส่งคืนผ่านไปรษณีย์/ขนส่ง เมื่อผู้ให้เช่าตรวจรับ เงินมัดจำจะโอนคืนอัตโนมัติเข้า PromptPay ภายใน 24 ชม.
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# 5. Top Header Navigation
# ==============================================================================
c_logo, c_nav, c_rent_btn, c_buy_btn, c_user = st.columns([3.2, 3.8, 1.4, 1.4, 2.2])

with c_logo:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:32px;">📚</span>
            <div>
                <span class="font-cute" style="font-size:24px; font-weight:700; color:#4A3528; line-height:1.1;">BookShare</span><br>
                <span style="font-size:11px; color:#8D7B68;">ร้านหนังสือ &amp; เช่ายืมออนไลน์</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c_nav:
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("หน้าแรก", key="nav_h", use_container_width=True):
            st.session_state.current_view = 'home'
            st.rerun()
    with n2:
        if st.button("สำรวจหนังสือ", key="nav_e", use_container_width=True):
            st.session_state.current_view = 'home'
            st.rerun()
    with n3:
        if st.button("วิธียืม-คืน", key="nav_hw", use_container_width=True):
            how_it_works_dialog()
    with n4:
        if st.button("สำหรับผู้ขาย/ผู้ให้เช่า", key="nav_s", use_container_width=True):
            st.session_state.current_view = 'seller'
            st.session_state.seller_subview = 'shelf'
            st.rerun()

with c_rent_btn:
    st.markdown("<div class='btn-cart-rent'>", unsafe_allow_html=True)
    if st.button(f"📖 ยืม {len(st.session_state.cart_rent)}", key="btn_top_rent", use_container_width=True):
        st.session_state.current_view = 'cart'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with c_buy_btn:
    st.markdown("<div class='btn-cart-buy'>", unsafe_allow_html=True)
    if st.button(f"🛍️ ซื้อ {len(st.session_state.cart_buy)}", key="btn_top_buy", use_container_width=True):
        st.session_state.current_view = 'cart'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with c_user:
    if st.session_state.user['logged_in']:
        u_col_av, u_col_nm = st.columns([1, 2.5])
        with u_col_av:
            st.markdown(
                """
                <div style="width:36px; height:36px; border-radius:50%; background-color:#E8DDD0; display:flex; align-items:center; justify-content:center; font-weight:700; color:#4A3528; border:1px solid #D5C5B5;">
                    M
                </div>
                """,
                unsafe_allow_html=True
            )
        with u_col_nm:
            st.markdown(
                f"""
                <div style="line-height:1.2; font-size:12px;">
                    <b>{st.session_state.user['name']}</b><br>
                    <span style="font-size:10px; color:#588157;">● {st.session_state.user['tier']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        if st.button("🔑 เข้าสู่ระบบ", key="btn_top_login", use_container_width=True):
            login_dialog()

st.markdown("<hr style='border:0; border-top:1px solid #EADBCE; margin:8px 0 20px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW 1: HOME PAGE
# ==============================================================================
if st.session_state.get('toast_msg'):
    st.toast(st.session_state.pop('toast_msg'), icon="🎉")

if st.session_state.current_view == 'home':
    col_srch, col_to_cart = st.columns([4, 1.2])
    with col_srch:
        st.session_state.search_query = st.text_input(
            "ค้นหา",
            value=st.session_state.search_query,
            placeholder="🔍 ค้นหาชื่อหนังสือ, ผู้แต่ง, หรือหมวดหมู่...",
            label_visibility="collapsed"
        )
    with col_to_cart:
        if st.button("👜 ไปที่ตะกร้าสินค้า", use_container_width=True):
            st.session_state.current_view = 'cart'
            st.rerun()

    # Hero Banner
    col_ht, col_hc = st.columns([1.8, 1.2])
    with col_ht:
        st.markdown(
            """
            <div class="hero-container">
                <span class="hero-badge">🌱 ชุมชนนักอ่านและการแบ่งปันหนังสือยั่งยืน</span>
                <div class="hero-h1">
                    ส่งต่อเรื่องราวดีๆ <br>
                    <u>อ่านเพลินไม่ต้องซื้อขาด</u> <br>
                    หรือสร้างรายได้จากตู้หนังสือ
                </div>
                <div class="hero-desc">
                    เช่ายืมเริ่มต้นเพียง <b>฿5 /วัน</b> ดื่มด่ำวรรณกรรมชิ้นโปรดแบบสบายกระเป๋า พร้อมส่งฟรีถึงประตูบ้านเมื่อเช่าครบ 3 เล่มขึ้นไป
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_hc:
        st.markdown(
            """
            <div style="background-color:#FFFFFF; border:1px solid #E8DDD0; border-radius:24px; padding:16px; box-shadow:0 6px 20px rgba(61,46,36,0.05); text-align:center;">
                <div style="position:relative; border-radius:16px; overflow:hidden; margin-bottom:12px;">
                    <img src="https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80" style="width:100%; height:200px; object-fit:cover;">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Categories
    st.markdown("<h3 style='margin:10px 0 6px 0; font-size:20px; color:#4A3528;'>หมวดหมู่ยอดนิยม</h3>", unsafe_allow_html=True)
    cats = ["ทั้งหมด", "📘 หนังสือของคุณ", "วรรณกรรม & นิยายแปล", "จิตวิทยา & พัฒนาตนเอง", "ธุรกิจ & การลงทุน", "หนังสือภาพ & ไลฟ์สไตล์"]
    c_cols = st.columns(len(cats))
    for i, c in enumerate(cats):
        with c_cols[i]:
            lbl = f"✓ {c}" if st.session_state.active_category == c else c
            if st.button(lbl, key=f"cat_sel_{i}", use_container_width=True):
                st.session_state.active_category = c
                st.rerun()

    # Filter books
    f_books = []
    for b in st.session_state.all_books:
        if st.session_state.active_category == "📘 หนังสือของคุณ":
            if not b.get('is_my_book', False):
                continue
        elif st.session_state.active_category != "ทั้งหมด" and b['category'] != st.session_state.active_category:
            continue
            
        if st.session_state.search_query:
            q = st.session_state.search_query.lower()
            if q not in b['title'].lower() and q not in b['author'].lower() and q not in b['category'].lower():
                continue
        f_books.append(b)

    st.markdown(f"<div style='margin:16px 0 10px 0;'><b style='font-size:18px; color:#4A3528;'>รายการหนังสือ ({len(f_books)} เล่ม)</b></div>", unsafe_allow_html=True)

    if not f_books:
        st.info("ไม่พบรายการหนังสือในหมวดหมู่นี้")
    else:
        grid_cols = st.columns(4)
        for idx, book in enumerate(f_books):
            col_pos = idx % 4
            with grid_cols[col_pos]:
                if book.get('is_my_book', False):
                    badge_html = "<span class='badge-mybook'>📘 หนังสือของคุณ</span>"
                elif book['status'] == 'available':
                    badge_html = "<span class='badge-available'>🟢 พร้อมให้ยืม</span>"
                elif book['status'] == 'rented':
                    badge_html = "<span class='badge-rented'>🔴 ถูกยืมอยู่</span>"
                else:
                    badge_html = "<span class='badge-sale'>🏷️ สำหรับขายเท่านั้น</span>"

                price_html = f"<div><span style='font-size:10px; color:#8D7B68;'>ยืม ฿{book['rent_price']}/วัน</span><br><b style='font-size:14px; color:#4A3528;'>ซื้อ ฿{book['buy_price']}</b></div>"

                st.markdown(
                    f"""
                    <div class="card-book">
                        <div style="position:relative;">
                            <img src="{book['img']}" class="book-cover-img" alt="{book['title']}">
                            <div style="position:absolute; top:6px; left:6px;">{badge_html}</div>
                            <div style="position:absolute; bottom:14px; right:6px;"><span class='badge-condition'>{book['condition']}</span></div>
                        </div>
                        <div style="font-size:11px; color:#8D7B68;">{book['category']}</div>
                        <h4 style="margin:2px 0 4px 0; font-size:13px; font-weight:700; color:#382B24; height:36px; overflow:hidden; line-height:1.3;">
                            {book['title']}
                        </h4>
                        <div style="font-size:11px; color:#6C5E53; margin-bottom:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                            {book['author']}
                        </div>
                        <div style="border-top:1px solid #EADBCE; padding-top:8px; margin-top:4px;">
                            {price_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                btn_txt = "🔍 ดูรายละเอียด" if book.get('is_my_book') else "🔍 ดูรายละเอียด & สั่งซื้อ"

                if st.button(btn_txt, key=f"btn_bk_{book['id']}", use_container_width=True):
                    st.session_state.selected_book_id = book['id']
                    st.session_state.current_view = 'detail'
                    st.rerun()

                st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW 2: BOOK DETAIL PAGE
# ==============================================================================
elif st.session_state.current_view == 'detail':
    book = get_book(st.session_state.selected_book_id)

    b1, b2 = st.columns([1.5, 8.5])
    with b1:
        if st.button("← กลับหน้าหลัก", key="back_home_btn"):
            st.session_state.current_view = 'home'
            st.rerun()
    with b2:
        st.markdown(f"<div style='font-size:13px; color:#8D7B68; padding-top:6px;'>หน้าแรก / หมวด {book['category']} / <b style='color:#4A3528;'>{book['title']}</b></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([4.2, 5.8], gap="large")

    with col_l:
        st.markdown(
            f"""
            <div style="position:relative; background-color:#FFFFFF; border:1px solid #EADBCE; border-radius:20px; overflow:hidden; padding:16px; text-align:center;">
                <img src="{book['img']}" style="width:100%; max-height:400px; object-fit:contain; border-radius:14px;">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_r:
        if book.get('is_my_book', False):
            st.warning("🔒 หนังสือเล่มนี้เป็นหนังสือที่คุณลงทะเบียนเข้าระบบ สามารถเข้าดูรายละเอียดได้เท่านั้น ไม่สามารถสั่งซื้อหรือเช่าได้")

        st.markdown(
            f"""
            <h2 style="margin:0 0 4px 0; font-size:24px; color:#4A3528; line-height:1.2;">{book.get('full_title', book['title'])}</h2>
            <div style="font-size:12px; color:#6C5E53; margin-bottom:10px;">ผู้แต่ง: {book['author']} | หมวดหมู่: {book['category']}</div>
            <p style="font-size:12px; color:#4A3528; line-height:1.6; background-color:#FAF6F0; padding:10px 14px; border-radius:12px; border:1px solid #EADBCE;">
                {book['desc']}
            </p>
            """,
            unsafe_allow_html=True
        )

        if not book.get('is_my_book', False):
            mode_choice = st.radio(
                "เลือกรูปแบบที่ต้องการ",
                options=['rent', 'buy'],
                format_func=lambda x: f"📖 ยืมอ่าน (฿{book['rent_price']}/วัน + มัดจำ ฿{book['deposit']})" if x == 'rent' else f"🛍️ ซื้อขาด (฿{book['buy_price']})",
                key=f"mode_choice_{book['id']}"
            )

            if mode_choice == 'rent':
                rent_days = st.slider("จำนวนวันที่ต้องการยืม", min_value=3, max_value=30, value=7)
                st.info(f"ค่ายืมรวม: ฿{book['rent_price'] * rent_days} (มัดจำคืนได้: ฿{book['deposit']})")

            if st.button("🛒 เพิ่มลงในตะกร้า", use_container_width=True):
                if mode_choice == 'rent':
                    st.session_state.cart_rent.append({
                        'id': book['id'], 'title': book['title'], 'author': book['author'],
                        'condition': book['condition'], 'rent_days': rent_days, 'start_date': str(date.today()),
                        'return_date': str(date.today() + timedelta(days=rent_days)), 'rate_per_day': book['rent_price'],
                        'total_rent': book['rent_price'] * rent_days, 'deposit': book['deposit'], 'img': book['img']
                    })
                else:
                    st.session_state.cart_buy.append({
                        'id': book['id'], 'title': book['title'], 'author': book['author'],
                        'condition': book['condition'], 'buy_price': book['buy_price'],
                        'original_price': book['original_price'], 'img': book['img']
                    })
                st.toast("เพิ่มลงในตะกร้าเรียบร้อยแล้ว!", icon="🛒")
        else:
            st.button("🚫 ไม่สามารถกดสั่งซื้อหนังสือของตัวเองได้", disabled=True, use_container_width=True)

# ==============================================================================
# 8. VIEW 3: CART & CHECKOUT PAGE
# ==============================================================================
elif st.session_state.current_view == 'cart':
    st.markdown("<h2>👜 ตะกร้าสินค้าและการชำระเงิน</h2>", unsafe_allow_html=True)
    
    tot_cnt = len(st.session_state.cart_rent) + len(st.session_state.cart_buy)
    if tot_cnt == 0:
        st.info("ตะกร้าสินค้าของคุณยังว่างอยู่ ลองไปเลือกชมหนังสือหน้าแรกดูสิ!")
        if st.button("← เลือกชมหนังสือ"):
            st.session_state.current_view = 'home'
            st.rerun()
    else:
        c_left, c_right = st.columns([6, 4], gap="large")
        
        with c_left:
            if st.session_state.cart_rent:
                st.markdown("### 📖 รายการยืมหนังสือ")
                for i, r_item in enumerate(st.session_state.cart_rent):
                    st.markdown(f"**{r_item['title']}** ({r_item['rent_days']} วัน)")
                    st.write(f"ค่ายืม: ฿{r_item['total_rent']} | ค่ามัดจำ: ฿{r_item['deposit']}")
                    if st.button(f"ลบรายการเช่าที่ {i+1}", key=f"del_r_{i}"):
                        st.session_state.cart_rent.pop(i)
                        st.rerun()
                    st.markdown("---")

            if st.session_state.cart_buy:
                st.markdown("### 🛍️ รายการซื้อขาด")
                for j, b_item in enumerate(st.session_state.cart_buy):
                    st.markdown(f"**{b_item['title']}** - ฿{b_item['buy_price']}")
                    if st.button(f"ลบรายการซื้อที่ {j+1}", key=f"del_b_{j}"):
                        st.session_state.cart_buy.pop(j)
                        st.rerun()
                    st.markdown("---")

        with c_right:
            st.markdown("<div style='background-color:#FFFFFF; border:1px solid #EADBCE; border-radius:16px; padding:20px;'>", unsafe_allow_html=True)
            st.markdown("### 📋 สรุปยอดชำระ")
            
            rent_sum = sum(x['total_rent'] for x in st.session_state.cart_rent)
            deposit_sum = sum(x['deposit'] for x in st.session_state.cart_rent)
            buy_sum = sum(x['buy_price'] for x in st.session_state.cart_buy)
            grand_total = rent_sum + deposit_sum + buy_sum

            st.write(f"ค่าบริการยืมรวม: ฿{rent_sum}")
            st.write(f"เงินมัดจำรวม (ได้รับคืนเมื่อส่งคืนหนังสือ): ฿{deposit_sum}")
            st.write(f"ราคาสินค้าสั่งซื้อรวม: ฿{buy_sum}")
            st.markdown(f"### **ยอดสุทธิ: ฿{grand_total}**")

            if st.button("💳 ยืนยันการสั่งซื้อและชำระเงิน", use_container_width=True):
                st.session_state.last_order = {
                    'rent_items': st.session_state.cart_rent.copy(),
                    'buy_items': st.session_state.cart_buy.copy(),
                    'total': grand_total
                }
                st.session_state.cart_rent = []
                st.session_state.cart_buy = []
                st.session_state.current_view = 'order_success'
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 9. VIEW 4: ORDER SUCCESS PAGE
# ==============================================================================
elif st.session_state.current_view == 'order_success':
    st.balloons()
    st.success("🎉 ชำระเงินและทำรายการสำเร็จ!")
    st.markdown("ทางเรากำลังเตรียมการจัดส่งหนังสือให้คุณอย่างเร็วที่สุด")
    
    if st.button("← กลับสู่หน้าหลัก", use_container_width=True):
        st.session_state.current_view = 'home'
        st.rerun()

# ==============================================================================
# 10. VIEW 5: SELLER CENTER & MY BOOKSHELF (Image 1 & Image 3)
# ==============================================================================
elif st.session_state.current_view == 'seller':
    if st.session_state.seller_subview == 'shelf':
        # Breadcrumbs & Trust Row
        b_c1, b_c2 = st.columns([6, 4])
        with b_c1:
            st.markdown(
                """
                <div style='font-size:12px; color:#8D7B68; padding-top:4px;'>
                    <a href='#' style='color:#8D7B68; text-decoration:none;'>หน้าแรก</a> / 
                    <span>บัญชีของฉัน</span> / 
                    <b style='color:#4A3528;'>คลังหนังสือของฉัน</b>
                </div>
                """,
                unsafe_allow_html=True
            )
        with b_c2:
            st.markdown(
                """
                <div style='text-align:right;'>
                    <span style='background-color:#EAF2E8; color:#2F5930; border:1px solid #C0DAC0; padding:4px 12px; border-radius:999px; font-size:11px; font-weight:600;'>
                        🟢 ระบบความคุ้มครอง BookShare Trust พร้อมดูแลหนังสือทุกเล่ม
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Header Title Banner Card matching Image 1
        c_head_l, c_head_r = st.columns([7, 3], gap="medium")
        total_cnt = len(st.session_state.shelf_books)
        rented_cnt = sum(1 for b in st.session_state.shelf_books if b['status'] == 'rented')
        avail_cnt = sum(1 for b in st.session_state.shelf_books if 'avail' in b['status'])
        private_cnt = sum(1 for b in st.session_state.shelf_books if b['status'] == 'private')

        with c_head_l:
            st.markdown(
                f"""
                <div style="background-color:#FFFFFF; border:1px solid #EADBCE; border-radius:24px; padding:22px; margin:10px 0 16px 0;">
                    <span style="background-color:#FAF0E4; border:1px solid #ECD8C3; color:#9C5212; padding:3px 12px; border-radius:999px; font-size:11px; font-weight:600;">
                        🏪 ตู้หนังสือชุมชน • รหัสสมาชิก #BS-88421
                    </span>
                    <h2 style="font-size:26px; font-weight:700; color:#4A3528; margin:8px 0 4px 0; font-family:'Mali', cursive;">
                        คลังหนังสือของฉัน <span style="font-size:16px; font-weight:400; color:#8D7B68; font-family:'Kanit', sans-serif;">(My Bookshelf &amp; Collection)</span>
                    </h2>
                    <p style="font-size:12px; color:#6C5E53; margin-bottom:12px;">
                        จัดการหนังสือสะสม เปิดโอกาสแบ่งปันเรื่องราวแก่นักอ่านท่านอื่น พร้อมสร้างรายได้หมุนเวียนอย่างยั่งยืน
                    </p>
                    <div style="display:flex; flex-wrap:wrap; gap:8px;">
                        <span style="background-color:#FAF0E6; color:#9C5212; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:700;">ทั้งหมด {total_cnt} เล่ม</span>
                        <span style="background-color:#FDF4EB; color:#D97706; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600;">● กำลังถูกเช่ายืม {rented_cnt}</span>
                        <span style="background-color:#EAF3EA; color:#2F5930; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600;">● พร้อมเช่า/ขาย {avail_cnt}</span>
                        <span style="background-color:#F3F4F6; color:#6B7280; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600;">● อ่านส่วนตัว {private_cnt}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c_head_r:
            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
            if st.button("➕ เพิ่มหนังสือเข้าคลังใหม่", key="btn_add_to_shelf_top", use_container_width=True):
                st.session_state.seller_subview = 'add_book'
                st.session_state.edit_book_id = None # รีเซ็ตค่าเพื่อเปิดฟอร์มเปล่า
                reset_add_book_form()
                st.rerun()
            if st.button("📋 จัดหมวดหมู่ชั้นหนังสือ", key="btn_cat_shelf", use_container_width=True):
                st.toast("จัดหมวดหมู่ชั้นหนังสือเรียบร้อยแล้ว", icon="📋")

        # Search & Filter Controls matching Image 1
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #EADBCE; border-radius:20px; padding:16px; margin-bottom:16px;'>", unsafe_allow_html=True)
        col_s1, col_s2, col_s3 = st.columns([5, 3, 2])
        with col_s1:
            shelf_search = st.text_input("ค้นหาในคลัง", placeholder="🔍 ค้นหาตามชื่อหนังสือ, ผู้เขียน, สำนักพิมพ์ หรือ ISBN...", key="shelf_srch", label_visibility="collapsed")
        with col_s2:
            shelf_filter = st.selectbox("สถานะ", ["ทั้งหมด", "กำลังถูกเช่ายืม", "วางปล่อยเช่า / ขาย", "อ่านส่วนตัว / ซ่อนไว้"], key="shelf_stat", label_visibility="collapsed")
        with col_s3:
            shelf_cat_filter = st.selectbox("หมวดหมู่", ["ทุกหมวดหมู่", "จิตวิทยา", "บริหาร", "วรรณกรรม", "การเงิน"], key="shelf_cat", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        # Filter shelf books
        filtered_shelf = []
        for bk in st.session_state.shelf_books:
            if shelf_filter == "กำลังถูกเช่ายืม" and bk['status'] != 'rented':
                continue
            elif shelf_filter == "วางปล่อยเช่า / ขาย" and 'avail' not in bk['status']:
                continue
            elif shelf_filter == "อ่านส่วนตัว / ซ่อนไว้" and bk['status'] != 'private':
                continue
            
            if shelf_cat_filter != "ทุกหมวดหมู่" and shelf_cat_filter not in bk.get('category', ''):
                continue

            if shelf_search:
                q = shelf_search.lower()
                if q not in bk['title'].lower() and q not in bk['author'].lower():
                    continue

            filtered_shelf.append(bk)

        # 4-Column Grid matching Image 1
        if not filtered_shelf:
            st.info("ไม่พบรายการหนังสือในตัวกรองนี้")
        else:
            grid_cols = st.columns(4)
            for idx, bk in enumerate(filtered_shelf):
                col_pos = idx % 4
                with grid_cols[col_pos]:
                    # Top Badges
                    if bk['status'] == 'rented':
                        badge_html = "<span style='background-color:#F8EDEB; color:#9C382A; border:1px solid #F3D5CF; padding:2px 8px; border-radius:999px; font-size:10px; font-weight:700;'>🕒 ถูกยืมอยู่</span>"
                    elif bk['status'] == 'avail_rent_sale':
                        badge_html = "<span style='background-color:#EAF3EA; color:#2F5930; border:1px solid #C5DDC5; padding:2px 7px; border-radius:999px; font-size:10px; font-weight:700;'>🟢 พร้อมให้เช่า</span> <span style='background-color:#FAF0E6; color:#9C5212; border:1px solid #EAC8A8; padding:2px 6px; border-radius:999px; font-size:9px; font-weight:600;'>เปิดขายขาดด้วย</span>"
                    elif bk['status'] == 'avail_rent':
                        badge_html = "<span style='background-color:#EAF3EA; color:#2F5930; border:1px solid #C5DDC5; padding:2px 7px; border-radius:999px; font-size:10px; font-weight:700;'>🟢 พร้อมให้เช่า</span> <span style='background-color:#FEF3C7; color:#92400E; border:1px solid #FDE68A; padding:2px 6px; border-radius:999px; font-size:9px; font-weight:600;'>😄 มีคนรอคิว 2 คน</span>"
                    else:
                        badge_html = "<span style='background-color:rgba(0,0,0,0.6); color:#FFFFFF; padding:2px 8px; border-radius:999px; font-size:10px; font-weight:600;'>คลังหนังสือของ 🔒 ส่วนตัว</span>"

                    # Bottom Overlay on cover
                    overlay_html = ""
                    if bk.get('borrower_name'):
                        overlay_html = f"""
                        <div style="position:absolute; bottom:0; left:0; right:0; background:rgba(0,0,0,0.7); color:#FFFFFF; padding:6px 8px; font-size:10px; border-bottom-left-radius:12px; border-bottom-right-radius:12px; line-height:1.2;">
                            <div>ผู้ยืมปัจจุบัน: {bk['borrower_name']}</div>
                            <div style="color:#FDE68A; font-weight:600; margin-top:2px;">⏳ {bk.get('days_left', '')} | {bk.get('shipping', '')}</div>
                        </div>
                        """
                    elif bk.get('review_rating'):
                        overlay_html = f"""
                        <div style="position:absolute; bottom:8px; left:8px; background:rgba(0,0,0,0.6); color:#FDE68A; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:600;">
                            {bk['review_rating']}
                        </div>
                        """

                    st.markdown(
                        f"""
                        <div class="card-book">
                            <div style="position:relative; width:100%; aspect-ratio:3/4; border-radius:12px; overflow:hidden; background-color:#EFE9E2; margin-bottom:10px;">
                                <img src="{bk['img']}" style="width:100%; height:100%; object-fit:cover;">
                                <div style="position:absolute; top:8px; right:8px; text-align:right;">{badge_html}</div>
                                {overlay_html}
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:10px; color:#8D7B68; margin-bottom:2px;">
                                <span>{bk.get('category', 'หมวดหมู่ทั่วไป')}</span>
                                <span>{bk.get('year', 'พิมพ์ปี 2023')}</span>
                            </div>
                            <h4 style="margin:2px 0 2px 0; font-size:13px; font-weight:700; color:#382B24; height:36px; overflow:hidden; line-height:1.3;">
                                {bk['title']}
                            </h4>
                            <div style="font-size:11px; color:#6C5E53; margin-bottom:6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                {bk['author']}
                            </div>
                            <div style="display:flex; gap:4px; margin-bottom:8px;">
                                <span style="background-color:#F5EFE6; border:1px solid #EADBCE; padding:2px 6px; border-radius:4px; font-size:9px;">{bk.get('cond1', 'สภาพ 95%')}</span>
                                <span style="background-color:#F5EFE6; border:1px solid #EADBCE; padding:2px 6px; border-radius:4px; font-size:9px; color:#8D7B68;">{bk.get('cond2', 'สมบูรณ์')}</span>
                            </div>
                            <div style="border-top:1px solid #EADBCE; padding-top:6px; margin-top:2px; display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <span style="font-size:9px; color:#8D7B68; display:block;">{bk.get('rate_label', 'ค่าบริการ')}</span>
                                    <b style="font-size:11px; color:#4A3528;">{bk.get('rate_val', '-')}</b>
                                </div>
                                <div style="text-align:right;">
                                    <span style="font-size:9px; color:#8D7B68; display:block;">{bk.get('income_label', 'ทำเงินสะสม')}</span>
                                    <b style="font-size:11px; color:#BC6C25;">{bk.get('income_val', '-')}</b>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button("⚙️ ตั้งค่าหนังสือ", key=f"btn_edit_{bk['id']}", use_container_width=True):
                            st.session_state.edit_book_id = bk['id']
                            st.session_state.seller_subview = 'add_book'
                            st.rerun()
                    with btn_c2:
                        if st.button("🗑️ ลบหนังสือ", key=f"btn_del_{bk['id']}", use_container_width=True):
                            # ลบหนังสือออกจากคลัง (shelf_books) และหน้าแรก (all_books)
                            st.session_state.shelf_books = [b for b in st.session_state.shelf_books if b['id'] != bk['id']]
                            st.session_state.all_books = [b for b in st.session_state.all_books if b['id'] != bk['id']]
                            st.toast(f"ลบหนังสือ {bk['title']} สำเร็จ", icon="🗑️")
                            st.rerun()

                    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

        st.caption(f"กำลังแสดงหนังสือลำดับที่ 1 - {len(filtered_shelf)} จากทั้งหมด {len(st.session_state.shelf_books)} เล่มในตู้หนังสือของคุณ")

    elif st.session_state.seller_subview == 'add_book':
        k_suf = st.session_state.form_key_suffix

        # ดึงข้อมูลหนังสือเดิมถ้าอยู่ในโหมดแก้ไข
        edit_bk = None
        edit_bk_all = None
        if st.session_state.edit_book_id:
            edit_bk = next((b for b in st.session_state.shelf_books if b['id'] == st.session_state.edit_book_id), None)
            edit_bk_all = next((b for b in st.session_state.all_books if b['id'] == st.session_state.edit_book_id), None)

        page_title = "⚙️ ตั้งค่าและแก้ไขข้อมูลหนังสือ" if edit_bk else "📄 ลงทะเบียนหนังสือใหม่เข้าสู่ระบบ (Add New Book)"

        # Top return button
        back_col1, back_col2 = st.columns([3, 7])
        with back_col1:
            if st.button("← กลับไปที่คลังหนังสือของฉัน", key="btn_back_to_shelf"):
                st.session_state.seller_subview = 'shelf'
                st.session_state.edit_book_id = None
                st.rerun()
        with back_col2:
            st.markdown("<div style='text-align:right;'><span style='background-color:#EAF2E8; color:#2F5930; padding:4px 12px; border-radius:999px; font-size:11px; font-weight:600;'>🛡️ มีระบบคุ้มครองประกันมัดจำ BookShare</span></div>", unsafe_allow_html=True)

        st.markdown(f"<h2>{page_title}</h2>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #EADBCE; border-radius:24px; padding:24px;'>", unsafe_allow_html=True)
        
        col_form_left, col_form_right = st.columns([4.2, 5.8], gap="large")

        with col_form_left:
            st.markdown("<b style='font-size:13px;'>อัปโหลดรูปภาพหนังสือจริง *</b>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพหนังสือ (JPG, PNG)", type=["jpg", "png", "jpeg"], key=f"upl_{k_suf}")
            
            # ใช้รูปเดิมถ้ามี หรือใช้รูปตัวอย่าง
            uploaded_img_url = edit_bk['img'] if edit_bk else "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80"
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="รูปภาพหนังสือที่คุณอัปโหลด", use_container_width=True)
                bytes_data = uploaded_file.getvalue()
                try:
                    import io
                    from PIL import Image
                    img_pil = Image.open(io.BytesIO(bytes_data)).convert("RGB")
                    img_pil.thumbnail((800, 800))
                    buf = io.BytesIO()
                    img_pil.save(buf, format="JPEG", quality=80)
                    uploaded_img_url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
                except Exception:
                    uploaded_img_url = "data:image/png;base64," + base64.b64encode(bytes_data).decode()
            else:
                st.image(uploaded_img_url, width=140, caption="ภาพปกปัจจุบัน" if edit_bk else "ตัวอย่างภาพปก")

            condition_val = st.select_slider("สภาพหนังสือ", options=["70% เก่าเก็บ", "85% ปานกลาง", "95% ดีมาก", "100% มือหนึ่ง"], value="95% ดีมาก", key=f"cond_{k_suf}")

        with col_form_right:
            b_title_input = st.text_input("ชื่อหนังสือ (Book Title) *", value=edit_bk['title'] if edit_bk else "", placeholder="กรอกชื่อหนังสือ...", key=f"title_{k_suf}")
            
            # ทำความสะอาดชื่อผู้แต่งเดิมที่อาจมีคำว่า 'โดย ' ติดมา
            def_author = edit_bk['author'].replace('โดย ', '') if edit_bk else ""
            b_author_input = st.text_input("ผู้แต่ง (Author) *", value=def_author, placeholder="กรอกชื่อผู้แต่ง...", key=f"auth_{k_suf}")
            
            cats = ["จิตวิทยา & พัฒนาตนเอง", "วรรณกรรม & นิยายแปล", "ธุรกิจ & การลงทุน", "หนังสือภาพ & ไลฟ์สไตล์"]
            def_cat_index = cats.index(edit_bk['category']) if edit_bk and edit_bk['category'] in cats else 0
            b_cat_input = st.selectbox("หมวดหมู่หนังสือ *", cats, index=def_cat_index, key=f"cat_{k_suf}")

            p_col1, p_col2 = st.columns(2)
            with p_col1:
                def_price = edit_bk_all['buy_price'] if edit_bk_all else 200
                price_sale = st.number_input("ราคาขายส่งต่อ (฿)", min_value=0, value=def_price, key=f"psale_{k_suf}")
            with p_col2:
                def_rent = edit_bk_all['rent_price'] if edit_bk_all else 5
                price_rent = st.number_input("ค่าเช่าต่อวัน (฿/วัน)", min_value=0, value=def_rent, key=f"prent_{k_suf}")

            def_desc = edit_bk_all['desc'] if edit_bk_all else ""
            b_desc_input = st.text_area("คำอธิบายหนังสือโดยย่อ", value=def_desc, placeholder="กรอกเรื่องย่อหรือรายละเอียดเพิ่มเติม...", key=f"desc_{k_suf}")

            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

            btn_text = "💾 บันทึกการเปลี่ยนแปลง" if edit_bk else "💾 บันทึกและลงทะเบียนหนังสือ"
            if st.button(btn_text, key=f"btn_sub_{k_suf}", use_container_width=True):
                if not b_title_input or not b_author_input:
                    st.error("กรุณากรอกชื่อหนังสือและผู้แต่งให้เรียบร้อย")
                else:
                    if edit_bk:
                        # อัปเดตข้อมูลเดิม
                        edit_bk['title'] = b_title_input
                        edit_bk['author'] = f"โดย {b_author_input}"
                        edit_bk['category'] = b_cat_input
                        edit_bk['img'] = uploaded_img_url
                        edit_bk['cond1'] = f"สภาพ {condition_val.split()[0]}"
                        edit_bk['rate_label'] = f"เช่า ฿{price_rent}/วัน"
                        edit_bk['rate_val'] = f"หรือขายขาด ฿{price_sale}"
                        
                        if edit_bk_all:
                            edit_bk_all['title'] = b_title_input
                            edit_bk_all['author'] = b_author_input
                            edit_bk_all['category'] = b_cat_input
                            edit_bk_all['img'] = uploaded_img_url
                            edit_bk_all['buy_price'] = price_sale
                            edit_bk_all['rent_price'] = price_rent
                            edit_bk_all['desc'] = b_desc_input

                        st.session_state['toast_msg'] = f"อัปเดตข้อมูล '{b_title_input}' สำเร็จ!"
                    else:
                        # ลงทะเบียนเล่มใหม่ (โค้ดเดิม)
                        new_id = len(st.session_state.all_books) + 1
                        new_book_item = {
                            'id': new_id,
                            'title': b_title_input,
                            'full_title': f"{b_title_input} (หนังสือของคุณ)",
                            'author': b_author_input,
                            'category': b_cat_input,
                            'isbn': '978-616-XXXXX-X',
                            'status': 'my_book',
                            'status_text': '📘 หนังสือของคุณ',
                            'condition': condition_val.split()[0],
                            'condition_full': condition_val,
                            'buy_price': price_sale,
                            'original_price': price_sale + 50,
                            'rent_price': price_rent,
                            'deposit': 100,
                            'img': uploaded_img_url,
                            'desc': b_desc_input if b_desc_input else "หนังสือที่คุณลงทะเบียนเข้าระบบด้วยตนเอง",
                            'seller_name': st.session_state.user['name'],
                            'seller_rating': 5.0,
                            'seller_count': 1,
                            'is_my_book': True
                        }
                        st.session_state.all_books.insert(0, new_book_item)
                        st.session_state.shelf_books.insert(0, {
                            'id': new_id,
                            'title': b_title_input,
                            'author': f"โดย {b_author_input}",
                            'category': b_cat_input,
                            'year': 'พิมพ์ปี 2024',
                            'img': uploaded_img_url,
                            'status': 'avail_rent_sale',
                            'cond1': f"สภาพ {condition_val.split()[0]}",
                            'cond2': 'ลงทะเบียนใหม่',
                            'rate_label': f"เช่า ฿{price_rent}/วัน",
                            'rate_val': f"หรือขายขาด ฿{price_sale}",
                            'income_label': 'ทำเงินสะสมแล้ว',
                            'income_val': '฿0 (เพิ่งลงระบบ)',
                            'btn1': '👁️ สถานะเปิดอยู่',
                            'btn2': '⚙️ ปรับราคา'
                        })
                        st.session_state['toast_msg'] = f"ลงทะเบียน '{b_title_input}' สำเร็จและเพิ่มเข้าคลังหนังสือแล้ว!"
                    
                    st.session_state.edit_book_id = None
                    st.session_state.seller_subview = 'shelf'
                    reset_add_book_form()
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)