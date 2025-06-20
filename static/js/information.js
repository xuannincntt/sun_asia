// Lấy các phần tử
const openImg = document.getElementById("openImgPopup");
const openName = document.getElementById("openNamePopup");
const openEmail = document.getElementById("openEmailPopup");
const openPassword = document.getElementById("openPassPopup");
const openPhone = document.getElementById("openPhonePopup");
const openAddress = document.getElementById("openAddressPopup");
const openUpdateAddress = document.querySelectorAll("openUpdateAddress");
const openDeleteAddress = document.querySelectorAll("openDeleteAddress");

const closeImg = document.getElementById("closeImgPopup");
const closeName = document.getElementById("closeNamePopup");
const closeEmail = document.getElementById("closeEmailPopup");
const closePassword = document.getElementById("closePassPopup");
const closePhone = document.getElementById("closePhonePopup");
const closeAddress = document.getElementById("closeAddressPopup");
const closeNewPassword = document.getElementById("closeNewPassPopup");
const closeUpdateAddress = document.getElementById("closeUpdateAddress");
const closeDeleteAddress = document.getElementById("closeDeleteAddress");

const imgPopup = document.getElementById("img-popup");
const namePopup = document.getElementById("name-popup");
const emailPopup = document.getElementById("email-popup");
const passwordPopup = document.getElementById("popupOverlayPass");
const passPopup = document.getElementById("pass-popup");
const newpassPopup = document.getElementById("newpass-popup");
const wrapperPass = document.getElementById("wrapperPass");
const phonePopup = document.getElementById("phone-popup");
const addressPopup = document.getElementById("address-popup");
const updateaddressPopup = document.getElementById("update-address-popup");
const deleteaddressPopup = document.getElementById("delete-address-popup");

const avatarImg = document.getElementById('avatarImg');
const avatarInitial = document.getElementById('avatarInitial');
const confirmButton = document.getElementById('confirmUpload');
const cancelButton = document.getElementById('cancelUpload');
let selectedFile = null;
// Lưu trạng thái ban đầu
const oldAvatarSrc = avatarImg.src;
const initialSrc = avatarImg.getAttribute('data-initial-src');
const hadAvatarInitially = initialSrc && initialSrc.trim() !== '';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Reset các input và thông báo lỗi
function resetPasswordForm() {
    document.getElementById('inf-pass').value = '';
    document.getElementById('update_pass').innerText = '';
    document.getElementById('inf-newpass').value = '';
    document.getElementById('update_newpass').innerText = '';
    document.getElementById('re-inf-newpass').value = '';
    document.getElementById('update_re_newpass').innerText = '';
    document.getElementById('pass-popup').style.display = 'block';
    document.getElementById('newpass-popup').style.display = 'none';
}

const csrfToken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", function () {
    const uploadDiv = document.getElementById('uploadDiv');
    const avatarInput = document.getElementById('avatarInput');
    // Khi click vào vùng upload thì trigger input file
    uploadDiv.addEventListener('click', () => {
        avatarInput.click();
    });

    /*================== name-popup ================== */
    // Mở popup khi click vào name-contain
    openImg.addEventListener("click", () => {
        imgPopup.style.display = "flex";
    });
    openName.addEventListener("click", () => {
        namePopup.style.display = "flex";
    });
    openEmail.addEventListener("click", () => {
        emailPopup.style.display = "flex";
    });
    openPassword.addEventListener("click", () => {
        passwordPopup.style.display = "flex";
    });
    openPhone.addEventListener("click", () => {
        console.log("Open phone popup");        
        phonePopup.style.display = "flex";
    });
    openAddress.addEventListener("click", () => {
        addressPopup.style.display = "flex";
    });
    // Khi mở popup
    // Gắn sự kiện khi mở popup
    document.querySelectorAll('.openUpdateAddress').forEach(button => {
        button.addEventListener('click', () => {
            updateaddressPopup.style.display = 'flex';
            const addressId = button.getAttribute('data-address-id');
            const provinceName = button.getAttribute('data-province');
            const districtName = button.getAttribute('data-district');
            const wardName = button.getAttribute('data-ward');
            const detail = button.getAttribute('data-detail');
            document.getElementById('update-detail_address').value = detail;
            document.querySelector('.updateAddress').setAttribute('data-address-id', addressId);
            const provinceSelect = document.getElementById('update-province');
            fetch('https://provinces.open-api.vn/api/?depth=1')
                .then(response => response.json())
                .then(data => {
                    provinceSelect.innerHTML = '<option value="">Tỉnh/Thành phố</option>';
                    let selectedProvinceCode = null;
                    data.forEach(province => {
                        const option = document.createElement('option');
                        option.value = province.code;
                        option.text = province.name;
                        provinceSelect.add(option);
                        if (province.name.trim().toLowerCase() === provinceName.trim().toLowerCase()) {
                            selectedProvinceCode = province.code;
                        }
                    });
                    if (selectedProvinceCode) {
                        provinceSelect.value = selectedProvinceCode;
                        loadDistricts(selectedProvinceCode, districtName, wardName);
                    }
                });
        });
    });
    // Khi chọn tỉnh mới
    document.getElementById('update-province').addEventListener('change', function () {
        const selectedProvinceCode = this.value;
        if (selectedProvinceCode) {
            loadDistricts(selectedProvinceCode, null, null);
        } else {
            // Reset nếu không chọn tỉnh
            document.getElementById('update-district').innerHTML = '<option value="">Quận/Huyện</option>';
            document.getElementById('update-ward').innerHTML = '<option value="">Phường/Xã</option>';
            document.getElementById('update-ward').disabled = true;
        }
    });
    // Khi chọn quận mới
    document.getElementById('update-district').addEventListener('change', function () {
        const selectedDistrictCode = this.value;
        if (selectedDistrictCode) {
            loadWards(selectedDistrictCode, null);
        } else {
            document.getElementById('update-ward').innerHTML = '<option value="">Phường/Xã</option>';
            document.getElementById('update-ward').disabled = true;
        }
    });
    // Hàm load quận/huyện
    function loadDistricts(provinceCode, selectedDistrictName, selectedWardName) {
        const districtSelect = document.getElementById('update-district');
        const wardSelect = document.getElementById('update-ward');
        districtSelect.innerHTML = '<option value="">Quận/Huyện</option>';
        wardSelect.innerHTML = '<option value="">Phường/Xã</option>';
        wardSelect.disabled = true;
        fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`)
            .then(response => response.json())
            .then(data => {
                let selectedDistrictCode = null;
                data.districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.code;
                    option.text = district.name;
                    districtSelect.add(option);
                    if (selectedDistrictName && district.name.trim().toLowerCase() === selectedDistrictName.trim().toLowerCase()) {
                        selectedDistrictCode = district.code;
                    }
                });
                if (selectedDistrictCode) {
                    districtSelect.value = selectedDistrictCode;
                    loadWards(selectedDistrictCode, selectedWardName);
                }
            });
    }
    // Hàm load phường/xã
    function loadWards(districtCode, selectedWardName) {
        const wardSelect = document.getElementById('update-ward');
        wardSelect.innerHTML = '<option value="">Phường/Xã</option>';
        fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`)
            .then(response => response.json())
            .then(data => {
                data.wards.forEach(ward => {
                    const option = document.createElement('option');
                    option.value = ward.code;
                    option.text = ward.name;
                    wardSelect.add(option);
                });
                // Enable phường/xã khi đã load xong
                wardSelect.disabled = false;
                if (selectedWardName) {
                    const wardOption = [...wardSelect.options].find(opt => opt.text.trim().toLowerCase() === selectedWardName.trim().toLowerCase());
                    if (wardOption) {
                        wardSelect.value = wardOption.value;
                    }
                }
            });
    }
    document.querySelectorAll('.openDeleteAddress').forEach(button => {
        button.addEventListener('click', () => {
            // Hiển thị popup xóa
            deleteaddressPopup.style.display = 'flex';
            // Lấy dữ liệu từ button (nếu cần lưu ID để xử lý xóa)
            const addressId = button.getAttribute('data-address-id');
            console.log('Selected addressId:', addressId);
            document.querySelector('.deleteAddress').setAttribute('data-address-id', addressId);
        });
    });
    // Đóng popup khi click vào nút đóng
    closeImg.addEventListener("click", () => {
        imgPopup.style.display = "none";
    });
    closeName.addEventListener("click", () => {
        namePopup.style.display = "none";
    });
    closeEmail.addEventListener("click", () => {
        emailPopup.style.display = "none";
    });
    closePassword.addEventListener("click", () => {
        passwordPopup.style.display = "none";
    });
    closeNewPassword.addEventListener("click", () => {
        passwordPopup.style.display = "none";
    });
    closePhone.addEventListener("click", () => {
        phonePopup.style.display = "none";
    });
    closeAddress.addEventListener("click", () => {
        addressPopup.style.display = "none";
    });
    closeUpdateAddress.addEventListener("click", () => {
        updateaddressPopup.style.display = "none";
    });
    closeDeleteAddress.addEventListener("click", () => {
        deleteaddressPopup.style.display = "none";
    });
    passPopup.addEventListener("click", () => {
        passwordPopup.classList.add("active-popup");
        wrapperPass.classList.add("active-popup");
        wrapperPass.classList.remove("active");
    });
    newpassPopup.addEventListener("click", () => {
        passwordPopup.classList.add("active-popup");
        wrapperPass.classList.add("active-popup");
        wrapperPass.classList.add("active");
    });
    // Đóng popup khi click ra ngoài
    window.addEventListener("click", (e) => {
        if (e.target === imgPopup) {
            imgPopup.style.display = "none";
        }
        if (e.target === namePopup) {
            namePopup.style.display = "none";
        }
        if (e.target === emailPopup) {
            emailPopup.style.display = "none";
        }
        if (e.target === passwordPopup) {
            passwordPopup.style.display = "none";
            wrapper.classList.remove("active-popup");
            popupOverlay.classList.remove("active-popup");
        }
        if (e.target === phonePopup) {
            phonePopup.style.display = "none";
        }
        if (e.target === addressPopup) {
            addressPopup.style.display = "none";
        }
        if (e.target === updateaddressPopup) {
            updateaddressPopup.style.display = "none";
        }
        if (e.target === deleteaddressPopup) {
            deleteaddressPopup.style.display = "none";
        }
    });
    /*================== avatar-update ================== */
    avatarInput.addEventListener('change', (event) => {
        if (event.target.files && event.target.files[0]) {
            selectedFile = event.target.files[0];
            uploadDiv.style.display = 'none'; // Ẩn vùng upload
            // Hiển thị ảnh preview
            const reader = new FileReader();
            reader.onload = function (e) {
                avatarImg.src = e.target.result;
                avatarImg.style.display = 'block';
                if (avatarInitial) {
                    avatarInitial.style.display = 'none';
                }
            };
            reader.readAsDataURL(selectedFile);
            // Hiển thị nút xác nhận / hủy
            confirmButton.style.display = 'inline-block';
            cancelButton.style.display = 'inline-block';
        }
    });
    // Khi nhấn Hủy
    cancelButton.addEventListener('click', () => {
        // Hiển thị lại vùng upload
        uploadDiv.style.display = 'flex';
        // Nếu ban đầu có avatar, khôi phục lại avatar cũ
        if (hadAvatarInitially) {
            avatarImg.src = oldAvatarSrc;
            avatarImg.style.display = 'block';
            if (avatarInitial) {
                avatarInitial.style.display = 'none';
            }
        } else { 
            // Nếu ban đầu không có avatar, khôi phục lại chữ cái
            avatarImg.src = '';
            avatarImg.style.display = 'none';
            if (avatarInitial) {
                avatarInitial.style.display = 'flex';
            }
        }
        // Ẩn nút
        confirmButton.style.display = 'none';
        cancelButton.style.display = 'none';
        // Reset input file
        avatarInput.value = '';
        selectedFile = null;
    });
    // Khi nhấn Xác nhận
    confirmButton.addEventListener('click', () => {
        if (selectedFile) {
            // Check
            console.log("Đã vào vòng lặp if else");
            const formData = new FormData();
            formData.append('avatar', selectedFile);
            fetch("/accounts/update-avatar/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log("Đã vào vòng lặp if else 2");
                if (data.success) {
                    alert('Cập nhật avatar thành công! ' + data.avatar_url);
                    avatarImg.style.display = 'block';
                    if (avatarInitial) {
                        avatarInitial.style.display = 'none';
                    }
                    uploadDiv.style.display = 'flex';
                    confirmButton.style.display = 'none';
                    cancelButton.style.display = 'none';
                    avatarInput.value = '';
                    selectedFile = null;
                    location.reload();
                } else {
                    alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Đã có lỗi xảy ra khi gửi request!');
            });
        }
    });
    /*================== name-update ================== */
    let saveName = document.querySelector(".saveName");
    saveName.addEventListener("click", () => {
        let newname = document.getElementById("name").value;
        let update_name = document.getElementById("update_name");
        fetch("/accounts/update-name/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ newname }),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cập nhật username thành công! ' + data.username);
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
                update_name.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
        });
    });
    /*================== email-update ================== */
    let saveEmail = document.querySelector(".saveEmail");
    saveEmail.addEventListener("click", () => {
        let newemail = document.getElementById("inf-email").value;
        let update_email = document.getElementById("update_email");
        fetch("/accounts/update-email/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ newemail }),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cập nhật email thành công! ' + data.email);
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
                update_email.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
            update_email.innerHTML = "<i class='bx bxs-error-circle'></i> " + error.error;
            location.reload();
        });
    });
    /*================== check pass ================== */
    document.querySelector(".savePass").addEventListener("click", () => {
        let password = document.getElementById("inf-pass").value;
        let updatePassMessage = document.getElementById("update_pass");
        fetch("/accounts/check-password/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("popupOverlayPass").classList.add("active-popup");
                document.getElementById("wrapperPass").classList.add("active-popup");
                document.getElementById("wrapperPass").classList.add("active");
            } else {
                updatePassMessage.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
            }
        })
        .catch(error => {
            updatePassMessage.innerHTML = "<i class='bx bxs-error-circle'></i> Lỗi kết nối tới server " + error;
            console.error("Error:", error);
        });
    });
    /*================== update pass ================== */
    document.querySelector(".saveNewPass").addEventListener("click", () => {
        const newPassword = document.getElementById("inf-newpass").value;
        const reNewPassword = document.getElementById("re-inf-newpass").value;
        const updatePassMessage = document.getElementById("update_newpass");
        const updateRePassMessage = document.getElementById("update_re_newpass");
        fetch("/accounts/update-password/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                newpassword: newPassword,
                "re-newpassword": reNewPassword
            })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cập nhật pass thành công! ' + data.pass);
                location.reload();
            }
            // Kiểm tra xem các ô mật khẩu có bị bỏ trống không
            if (!newPassword || !reNewPassword) {
                updatePassMessage.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
                return;
            }
            if (newPassword != reNewPassword) {
                updateRePassMessage.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
                return;
            }
        })
        .catch(error => {
            updatePassMessage.textContent = "Lỗi kết nối tới server!";
            console.error("Error:", error);
        });
    });
    /*================== phone-update ================== */
    let savePhone = document.querySelector(".savePhone");
    savePhone.addEventListener("click", () => {
        let newphone = document.getElementById("inf-phone").value;
        let update_phone = document.getElementById("update_phone");
        fetch("/accounts/update-phone/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ newphone }),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cập nhật phone thành công! ' + data.phone);
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
                update_phone.innerHTML = "<i class='bx bxs-error-circle'></i> " + data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
        });
    });
    /*================== address-create ================== */
    const provinceSelect = document.getElementById('province');
    const districtSelect = document.getElementById('district');
    const wardSelect = document.getElementById('ward');
    const detailInput = document.getElementById('detail_address');
    // Load Tỉnh/Thành phố
    fetch('https://provinces.open-api.vn/api/?depth=1')
        .then(response => response.json())
        .then(data => {
            data.forEach(province => {
                const option = document.createElement('option');
                option.value = province.code;
                option.text = province.name;
                provinceSelect.add(option);
            });
        });
    provinceSelect.addEventListener('change', function () {
        districtSelect.length = 1;
        wardSelect.length = 1;
        districtSelect.disabled = wardSelect.disabled = true;
        const provinceCode = this.value;
        if (!provinceCode) return;
        districtSelect.disabled = false;
        fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`)
            .then(response => response.json())
            .then(data => {
                data.districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.code;
                    option.text = district.name;
                    districtSelect.add(option);
                });
            });
    });
    districtSelect.addEventListener('change', function () {
        wardSelect.length = 1;
        wardSelect.disabled = true;
        const districtCode = this.value;
        if (!districtCode) return;
        wardSelect.disabled = false;
        fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`)
            .then(response => response.json())
            .then(data => {
                data.wards.forEach(ward => {
                    const option = document.createElement('option');
                    option.value = ward.name;
                    option.text = ward.name;
                    wardSelect.add(option);
                });
            });
    });
    document.querySelector(".saveAddress").addEventListener("click", () => {
        const provinceText = provinceSelect.options[provinceSelect.selectedIndex]?.text || '';
        const districtText = districtSelect.options[districtSelect.selectedIndex]?.text || '';
        const wardText = wardSelect.options[wardSelect.selectedIndex]?.text || '';
        const detailAddress = detailInput.value.trim() || '';
        console.log("Province:", provinceText);
        console.log("District:", districtText);
        console.log("Ward:", wardText);
        console.log("Detail Address:", detailAddress);
        const newAddress = {
            province: provinceText,
            district: districtText,
            ward: wardText,
            detail: detailAddress
        };
        fetch("/accounts/create-address/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(newAddress),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cập nhật địa chỉ thành công!');
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
        });
    });

    /*================== set-default ================== */
    document.querySelectorAll('.btn-default').forEach(button => {
        button.addEventListener('click', () => {
            const addressId = button.getAttribute('data-address-id');

            fetch('/accounts/set-default-address/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ address_id: addressId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Đã thiết lập địa chỉ mặc định thành công!');
                    location.reload(); // Reload để cập nhật giao diện
                } else {
                    alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Đã có lỗi xảy ra khi gửi request!');
            });
        });
    });
    /*================== address-update ================== */
    document.querySelector('.updateAddress').addEventListener('click', () => {
        console.log("Hello Bach Rach");
        const addressId = document.querySelector('.updateAddress').getAttribute('data-address-id');
        const provinceSelect = document.getElementById('update-province');
        const province = provinceSelect.options[provinceSelect.selectedIndex].text;
        const districtSelect = document.getElementById('update-district');
        const district = districtSelect.options[districtSelect.selectedIndex].text;
        const wardSelect = document.getElementById('update-ward');
        const ward = wardSelect.options[wardSelect.selectedIndex].text;
        const detail = document.getElementById('update-detail_address').value;
        fetch('/accounts/update-address/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                address_id: addressId,
                province: province,
                district: district,
                ward: ward,
                detail: detail
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Cập nhật địa chỉ thành công!');
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
        });
    });
    /*================== address-delete ================== */
    document.querySelector('.deleteAddress').addEventListener('click', () => {
        console.log("Hello Bach Rach");
        const addressId = document.querySelector('.deleteAddress').getAttribute('data-address-id');
        fetch('/accounts/delete-address/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                address_id: addressId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Xóa địa chỉ thành công!');
                location.reload();
            } else {
                alert('Đã có lỗi xảy ra: ' + (data.error || 'Không rõ'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi gửi request!');
        });
    });
});
