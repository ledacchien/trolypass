import streamlit as st

# Thêm nút quay về trang chủ
st.page_link("streamlit_app.py", label="⬅️ Quay về Trang chủ")
st.divider()

# --- Nội dung bài viết ---
st.title("Đây là BÀI VIẾT SỐ 3")
st.header("Chủ đề: Lập trình và Phát triển 💻")
st.success("Nếu bạn thấy nội dung này, có nghĩa là link đã hoạt động!")
st.image("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=2070", caption="Những dòng code thay đổi thế giới.")
