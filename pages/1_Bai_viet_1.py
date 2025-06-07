import streamlit as st

# Thêm nút quay về trang chủ
st.page_link("streamlit_app.py", label="⬅️ Quay về Trang chủ")
st.divider()

# --- Nội dung bài viết ---
st.title("Đây là BÀI VIẾT SỐ 1")
st.header("Chủ đề: Du hành Vũ trụ 🚀")
st.success("Nếu bạn thấy nội dung này, có nghĩa là link đã hoạt động!")
st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072", caption="Trái Đất nhìn từ không gian.")
