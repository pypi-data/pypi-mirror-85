import os
import os.path
import datetime as dt
import shutil
from hashlib import scrypt
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchWindowException
import helium as he


class Npal():
    file = '.credential'

    @staticmethod
    def generate_cipher(userkey):
        salt = b'\xf9(&\xb3\xc9\xd1X\xd4\x94\xe6a$f\x88\xef\x8a'  # urandom(16)
        key = scrypt(userkey.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
        cipher = Fernet(urlsafe_b64encode(key))
        return cipher


    @classmethod
    def read_credential(cls, passphrase):
        if os.path.isfile(cls.file):
            with open(cls.file, 'rb') as f:
                npnet_id, password = f.read().split(b':', 1)

            cipher = Npal.generate_cipher(passphrase)
            try:
                password = cipher.decrypt(password)
                del cipher
                return (npnet_id.decode(), password.decode())
            except:
                del cipher
                return (None, None)
        else:
            return (None, None)


    @classmethod
    def write_credential(cls, passphrase):
        npnet_id = input('Enter NPnet ID: ')
        password = getpass('Enter password: ')
        cipher = Npal.generate_cipher(passphrase)
        password = cipher.encrypt(password.encode()).decode()
        with open(cls.file, 'w') as f: 
            f.write(f'{npnet_id}:{password}')
        return npnet_id, password


    @staticmethod
    def chrome_download_complete(driver):
        '''
        Monitor download completion
        '''
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")

        driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """
        )
        return True


    @staticmethod
    def chrome_prefs(download_dir):
        '''
        Change default download directory and behaviour
        '''
        options = ChromeOptions()
        options.add_experimental_option(
            'prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True
            }
        )
        return options


    @staticmethod
    def move_file(old_fullpathname, dest_dir, filename, overwrite=False):
        '''
        Move old_fullpathname to dest_dir/filename
        If overwrite is True and dirname(old_fullpathname)/filename exists, 
        the existing file will be overwritten. Otherwise the existing file
        will be renamed using timestamp.
        '''
        old_basename = os.path.dirname(old_fullpathname)
        #old_filename, old_ext = os.path.splitext(os.path.basename(old_fullpathname))
        new_filename, new_ext = os.path.splitext(filename)

        srcname = os.path.join(old_basename, new_filename+new_ext)
        dstname = os.path.join(dest_dir,     new_filename+new_ext)

        # If a file with the same name exists,
        if os.path.isfile(srcname):
            if overwrite == False:
            # Rename the file using current time
                now = str(dt.datetime.now())[:19]
                for c in ' :-': now = now.replace(c, '')
                srcname2 = os.path.join(old_basename, new_filename+'_'+now+new_ext)
                os.rename(srcname, srcname2)
            else:
                os.remove(srcname)

        # old_fullpathname -> srcname -> dstname
        os.rename(old_fullpathname, srcname)
        if srcname != dstname:
            shutil.move(srcname, dstname)


    @staticmethod
    def start_Npal(dest_dir, options=None):
        url = 'https://npalcs.np.edu.sg/psp/staff/EMPLOYEE/SA/h/?tab=DEFAULT&cmd=login&errorCode=106&languageCd=ENG'
        driver = he.start_chrome(url, options=Npal.chrome_prefs(dest_dir))
        if not os.path.isfile('.credential'):
            passphrase = getpass('Enter your secret passphrase: ')
            npnetid, password = Npal.write_credential(passphrase)
            del passphrase
        else:
            npnetid, password = Npal.read_credential(getpass('Enter your secret passphrase: '))
        Npal.write(npnetid, into='User Id')
        Npal.write(password, into='Password')
        Npal.click('Sign in')
        del password
        return driver


    @staticmethod
    def query_report(driver, script, dest_dir, filename, *args):
        try:
            driver.execute_script(script)
            driver.switch_to.window(driver.window_handles[1])
            Npal.wait_until(Npal.chrome_download_complete)
        except NoSuchWindowException:
            # The download has completed too quickly
            pass
        finally:
            old_filename = max([dest_dir + f for f in os.listdir(dest_dir)],key=os.path.getctime)
            Npal.move_file(old_filename, dest_dir, filename)
            print(f'Report is at {dest_dir}/{filename}')
            return True
        

    @staticmethod
    def write(text, into=None):
        he.write(text, into=into)


    @staticmethod
    def click(element):
        he.click(element)
        
        
    @staticmethod
    def wait_until(condition_fn, timeout_secs=10, interval_secs=0.5):
        he.wait_until(condition_fn, timeout_secs=timeout_secs, interval_secs=interval_secs)


    @staticmethod
    def close_browser():
        he.kill_browser()



if __name__ == '__main__':
    Npal.write_credential(getpass('Enter your secret passphrase: '))
    npnetid, password = Npal.read_credential(getpass('Enter your secret passphrase: '))
    print(f'npnet_id={npnetid}\npassword={password}')
