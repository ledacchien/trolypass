import streamlit as st

# Thêm nút quay về trang chủ
st.page_link("streamlit_app.py", label="⬅️ Quay về Trang chủ")
st.divider()

# --- Nội dung bài viết ---
st.title("Đây là BÀI VIẾT SỐ 2")
st.header("Chủ đề: Trí tuệ Nhân tạo (AI) 🤖")
st.success("Nếu bạn thấy nội dung này, có nghĩa là link đã hoạt động!")
st.image("https://images.unsplash.com/photo-1535378620166-273708d44e4c?q=80&w=1974", caption="AI và tương lai của công nghệ.")
