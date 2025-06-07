import streamlit as st
from openai import OpenAI, OpenAIError
import os
import glob

# --- CÁC HÀM TIỆN ÍCH ---

def rfile(name_file):
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return ""

def load_config_data(config_file, default_data):
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            while len(lines) < len(default_data):
                lines.append(default_data[len(lines)])
            return lines[:len(default_data)]
    except Exception:
        return default_data

def load_all_product_data(folder_path="product_data"):
    combined_data = []
    if not os.path.isdir(folder_path):
        return ""
    
    for file_path in glob.glob(os.path.join(folder_path, '*.txt')):
        content = rfile(file_path)
        if content:
            combined_data.append(content)
    
    return "\n\n---\n\n".join(combined_data)

# HÀM MỚI: Đọc tài khoản từ file credentials.txt
def load_credentials(file="credentials.txt"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) >= 2:
                return lines[0], lines[1] # Trả về (username, password)
    except Exception:
        pass
    return "thuenha", "thuenha" # Trả về giá trị mặc định nếu có lỗi


# --- HÀM KIỂM TRA ĐĂNG NHẬP ---

def check_login():
    if st.session_state.get("authenticated", False):
        return True

    st.title("🔐 Đăng nhập vào ứng dụng")
    username = st.text_input("Tên đăng nhập", key="login_user")
    password = st.text_input("Mật khẩu", type="password", key="login_pass")

    if st.button("Đăng nhập", key="login_button"):
        # Ưu tiên lấy tài khoản từ Heroku Secrets trước
        heroku_user = st.secrets.get("USERNAME")
        heroku_pass = st.secrets.get("PASSWORD")

        # Nếu không có trên Heroku, mới đọc từ file local
        local_user, local_pass = load_credentials()

        # Dùng tài khoản của Heroku nếu có, nếu không thì dùng của file local
        correct_username = heroku_user or local_user
        correct_password = heroku_pass or local_pass

        if username == correct_username and password == correct_password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không chính xác.")
    
    return False

# --- BẮT ĐẦU CHẠY APP ---

if not check_login():
    st.stop()

# --- NẾU ĐĂNG NHẬP THÀNH CÔNG, HIỂN THỊ NỘI DUNG ---

st.set_page_config(page_title="Trợ lý AI", page_icon="🤖", layout="centered")

default_images = ["https://placehold.co/300x200/a3e635/44403c?text=Ảnh+1", "https://placehold.co/300x200/facc15/44403c?text=Ảnh+2", "https://placehold.co/300x200/67e8f9/44403c?text=Ảnh+3"]
default_titles = ["Tiêu đề 1", "Tiêu đề 2", "Tiêu đề 3"]
image_urls = load_config_data("config_images.txt", default_images)
article_titles = load_config_data("config_titles.txt", default_titles)

# --- BỘ CSS HOÀN CHỈNH ---
st.markdown("""
<style>
    [data-testid="stToolbar"] {visibility: hidden !important;}
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stImage"]) > div[data-testid="stVerticalBlock"] { height: 100%; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] { display: flex; flex-direction: column; justify-content: space-between; height: 100%; }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stChatMessageContent-user"]) { justify-content: flex-end; }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent-user"]) { flex-direction: row-reverse; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.success("✅ Đã đăng nhập")
    if st.button("Đăng xuất"):
        del st.session_state["authenticated"]
        if "messages" in st.session_state:
            del st.session_state["messages"]
        st.rerun()

st.subheader("✨ Các bài viết nổi bật")

col1, col2, col3 = st.columns(3, gap="medium")
page_links = ["1_Bai_viet_1", "2_Bai_viet_2", "3_Bai_viet_3"]

for i, col in enumerate([col1, col2, col3]):
    with col:
        st.image(image_urls[i], use_container_width=True)
        st.markdown(f"<h4 style='text-align: center; margin-top: 1rem; flex-grow: 1;'>{article_titles[i]}</h4>", unsafe_allow_html=True)
        st.page_link(f"pages/{page_links[i]}.py", label="📄 Đọc chi tiết", use_container_width=True)

st.divider()

if os.path.exists("logo.png"):
    logo_cols = st.columns([2, 3, 2])
    with logo_cols[1]:
        st.image("logo.png", use_container_width=True)

title_content = rfile("00.xinchao.txt") or "Chào mừng đến với Trợ lý AI"
st.markdown(f"<h2 style='text-align: center;'>{title_content}</h2>", unsafe_allow_html=True)

openai_api_key = st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Chưa có OpenAI API Key. Vui lòng thêm vào st.secrets!")
    st.stop()
try:
    client = OpenAI(api_key=openai_api_key)
    client.models.list()
except OpenAIError as e:
    st.error(f"Lỗi xác thực OpenAI API Key: {e}. Vui lòng kiểm tra lại key.")
    st.stop()

if "messages" not in st.session_state:
    assistant_greeting = rfile("02.assistant.txt") or "Tôi có thể giúp gì cho bạn?"
    st.session_state.messages = [{"role": "assistant", "content": assistant_greeting}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    general_prompt = rfile("01.system_trainning.txt") or "Bạn là một trợ lý ảo hữu ích."
    product_keywords = ["căn hộ", "phòng", "giá", "diện tích", "ch00", "còn trống", "thuê", "tìm", "báo giá"]
    is_product_query = any(keyword in prompt.lower() for keyword in product_keywords)
    
    final_system_prompt = general_prompt
    if is_product_query:
        all_product_data = load_all_product_data("product_data")
        if all_product_data:
            final_system_prompt += "\n\nDưới đây là dữ liệu về các sản phẩm/căn hộ. Hãy dựa vào đây để trả lời câu hỏi của người dùng:\n" + all_product_data

    messages_to_send = [{"role": "system", "content": final_system_prompt}]
    messages_to_send.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("Trợ lý đang suy nghĩ..."):
            try:
                stream = client.chat.completions.create(
                    model=rfile("module_chatgpt.txt").strip() or "gpt-3.5-turbo",
                    messages=messages_to_send,
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except OpenAIError as e:
                st.error(f"Đã xảy ra lỗi với OpenAI: {e}")
