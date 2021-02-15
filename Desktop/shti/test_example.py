import pytest
import subprocess
import re

#pytest test_example.py -k test_info --file_path "C:\Users\Vlad\Desktop\shti\Av1tote.mp4" --mp4box_file_path "C:\Program Files\GPAC\mp4box.exe"
#pytest test_example.py  --file_path "C:\Users\Vlad\Desktop\shti\Av1tote.mp4" --mp4box_file_path "C:\Program Files\GPAC\mp4box.exe" -v --junitxml="result.xml"
@pytest.fixture(scope='module')
def input_file_path(request):
    return request.config.getoption("--file_path")

@pytest.fixture(scope='module')
def mp4box_file_path(request):
    return request.config.getoption("--mp4box_file_path")


    
def test_Info(input_file_path, mp4box_file_path):
    pattern = "AOM (.+) stream"  
    cmd = '"%s" -info "%s"'%(mp4box_file_path, input_file_path)
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
    stdout = p.communicate()[0]
    stdout = stdout.decode()
    rc = p.returncode
    assert(rc==0), 'cannot open thefile'
    result = re.findall(pattern,stdout)
    assert(result==['AV1']), 'Codec is not av1'
    
def test_ExtractFromFile(input_file_path, mp4box_file_path):
    pattern1 = "AOM (.+) stream"
    pattern2= "AOM (.+) Video"
    i=1
    result =""
    while result!=['AV1']:
        cmd = '"%s" -infon %d  "%s"'%(mp4box_file_path,i,input_file_path)  
        p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        stdout = p.communicate()[0]
        stdout = stdout.decode()
        rc = p.returncode
        assert(rc==0),'cannot find av1 file'
        result = re.findall(pattern1,stdout)
        
        rawid=i
        i+=1
        if result==['AV1']:
            cmd = '"%s" -raw %d  "%s" -out newvideo.avi'%(mp4box_file_path,rawid,input_file_path)
            a = subprocess.run(cmd)
            rc = a.returncode
            assert(rc==0),'cannot create the file'
    cmd = '"%s" -info newvideo.avi'%mp4box_file_path
    p = subprocess.Popen(cmd, shell= True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout = p.communicate()[0]
    stdout = stdout.decode()
    rc = p.returncode
    assert(rc==0), "Cant read info about newvideo"
    finresult = re.findall(pattern2,stdout)
    assert(finresult==['AV1']), 'Codec is not av1'

def test_AddToFile(mp4box_file_path):
    pattern="AOM (.+?) stream"
    pattern2="Track # (.+) Info "
    cmd = '"%s" -add  "av1tote_track2.av1" AnotherNewVideo.mp4'%(mp4box_file_path)
    p = subprocess.run(cmd)
    rc = p.returncode
    assert(rc==0), 'Error add track to mp4'
    cmd = '"%s" -info AnotherNewVideo.mp4'%mp4box_file_path
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout = p.communicate()[0]
    stdout = stdout.decode()
    rc = p.returncode
    assert(rc==0), 'Error read mp4'
    result = re.findall(pattern,stdout)
    assert(result[-1]=='AV1'), 'Codec is not av1'
    TrackId = re.findall(pattern2,stdout)
    KillNum = int(TrackId[-1])
    cmd = '"%s" -rem %d   AnotherNewVideo.mp4'%(mp4box_file_path, KillNum)
    p = subprocess.run(cmd)
    rc = p.returncode
    assert(rc==0),'Error remove last track'
   

    
def test_Crypto(input_file_path, mp4box_file_path):
  assert False, "I mean for this to fail"