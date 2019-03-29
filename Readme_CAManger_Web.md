# CAManger_Web

#### 목적

CertManager는 사설 CA를 만들고 사설 인증서를 발급 받기 위해 만들어졌습니다.

1. 인증서 발급을 위한 CSR을 생성하여
2. 인증서에 사인할 CA를 선택하여 신청한 후
3. 발급된 인증서를 다운받을 수 있습니다.

#### 설치

Centos7

##### 파이썬

<https://www.python.org/downloads/>

리눅스(Centos7)

```
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
```

```
yum search python36
```

```
yum install -y python36u python36u-libs python36u-devel python36u-pip
```

```
wget https://bootstrap.pypa.io
```

파이썬 패키지 라이브들을 설치하기 위해  pip 설치

```
python3.6 get-pip.py
```

```
yum install python-pip
```

```
pip install ez_setup
```

```
pip install unroll
```

고립된 환경을 위해 virtualenv 설치

```
pip install virtualenv
```

실행

```
. venv/bin/activate
```

장고 설치가 안되는 경우가 있으니 pip 업그레이드

```
pip install --upgrade pip
```

**django 설치**

```
sudo pip install django
```

**패키지** **설치**

```py
pip install -r requirements.txt
```

**실행** 

장고의 settings.py에 들어가 ALLOWED_HOSTS에 자신의 호스트를 추가 IP에 접근 할 수 있습니다.

```
vim mysite/settings.py
```

제 VM 아이피의 경우 192.168.206.137

```ALLOWED_HOSTS = [&#39;127.0.0.1&#39;,&#39;192.168.206.137&#39;,]
ALLOWED_HOSTS = ['127.0.0.1','192.168.206.137',]
```

이제 8000포트를 통해 실행해 봅시다.

```
python manage.py runserver 0.0.0.0:8000
```

로컬의 경우 127.0.0.1:8000을 브라우져의 URL창에 입력 합니다.

VM을 사용한경우(제 VM IP, 192.168.206.137) 192.168.206.137:8000를 입력합니다.



실행 화면

![1553833660147](C:\Users\Jay\AppData\Roaming\Typora\typora-user-images\1553833660147.png)



# CSR 생성

#### 목적

인증 받을 회사의 정보를 포함한 CSR을 만들기 위함 입니다.

이 CSR을 CA에게 제출하면 인증서를 발급 받을 수 있습니다.

#### 필요 인자

Organization : 자신의 회사 명

Organization_unit: 부서명

Country: 나라 선택

State: 시,도 선택

Locality: 군,구 선택

Common_name:  회사명

Domain: 회사의 URL



알고리즘을 선택합니다

RSA 2048  2. RSA 4096   3. ECDSA P256  4. ECDSA P384

#### 아웃풋

CSR을 다운 받을 수 있습니다.



# CA 생성

#### 목적

CA를 생성해 인증서에 서명하도록 합니다.

#### 필요 인자

Organization : 자신의 CA 명

Country: 나라 선택

State: 시,도 선택

Locality: 군,구 선택

Common_name:  CA명

Domain: CA의 URL



알고리즘을 선택합니다

RSA 2048  2. RSA 4096   3. ECDSA P256  4. ECDSA P384

#### 아웃풋

private key, public key, self signed certificate(테스트용)을 다운 받을 수 있습니다.





# 인증서 발급

#### 목적

CSR을 제출해 CA로부터 사인된인증서를 발급 받습니다.

#### 명령어

```python
python CAManager.py generatekey
```

#### 필요 인자

CSR을 생성해야 합니다.

CA를 선택해야 합니다.

#### 아웃풋

인증서 파일을 다운받을 수 있습니다.