<p><img src="https://raw.githubusercontent.com/darzanebor/cookie/master/img/pylint0.svg" title="pylint"></a>&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/darzanebor/cookie/master/img/pylint1.svg" title="pylint"></a>&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/darzanebor/cookie/master/img/pylint2.svg" title="pylint"></a>&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/darzanebor/cookie/master/img/pylint3.svg" title="pylint"></a>
</p>
<p align="center"><a href='https://github.com/darzanebor/cookie'><img src="https://raw.githubusercontent.com/darzanebor/cookie/master/img/logo.png" title="COOKIE"></a></p>
1) Thumbnail by PUT request:<br/><br/>
  curl -XPUT -F 'file=@./img/cat.jpg' -F 'scale=10' http://127.0.0.1:5000 --output 1.jpeg<br/><br/>
2) Thumbnail over GET request with image url:<br/>
- Url is base64 encoded string<br/>
    http://localhost:5000/?url=aHR0cHM6Ly9pY2hlZi5iYmNpLmNvLnVrL25ld3MvOTc2L2Nwc3Byb2RwYi8xMkE5Qi9wcm9kdWN0aW9uL18xMTE0MzQ0NjdfZ2V0dHlpbWFnZXMtMTE0MzQ4OTc2My5qcGc=<br/><br/>

<div align=center> 
<table border="0" cellpadding="0" cellspacing="0" border-collapse="collapse">
<tbody>
<tr>
<td>
  
| ENVIRONMENT VARIABLES | DEFAULT VALUE |
| ------------- | ------------- |
| COOKIE_HOST | 0.0.0.0 |
| COOKIE_PORT | 5000 |
| COOKIE_FIXED_SIZE (WIDTH)| 120 |
| COOKIE_DEFAULT_SCALE | 30 |
| COOKIE_IMAGE_MAX_SIZE | 31457280 (bytes) |
</td>
<td>
  
| HTTP Headers ||
| ------------- | ------------- |
| X-FORWARDED-PROTOCOL | ssl |
| X-FORWARDED-PROTO | https |
| X-FORWARDED-SSL | on |
| X-Orig-Hash (reply) | md5 sum |
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
</div>

By DEFAULT log format JSON.
