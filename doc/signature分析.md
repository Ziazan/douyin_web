<!--
 * @Author: your name
 * @Date: 2020-05-03 18:50:34
 * @LastEditTime: 2020-05-10 00:06:46
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /python/douyin_web/doc/url_info.md
 -->
# 抖音视频列表接口分析
https://www.iesdouyin.com/web/api/v2/aweme/post/
sec_uid: MS4wLjABAAAANMz0vsbHsID55ivkeXD0r4UddEmgUlBW1WPJuTjcsrspY4eRidlWqYlvi_xOWhs4
count: 21
max_cursor: 1587352073000
aid: 1128
_signature: -Xa3DhAdp-KKgL1hbkgL0Pl2tx
dytk: 2022333dcf2be9d7b323e189a4fdcfba 


## sec_uid ：
在这个文件中出现过
https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/page/reflow_user/index_10ae3b3.js:formatted
这个包里面定义了sec_uid:douyin_falcon:page/reflow_user/index 
的init 方法里面定义了，sec_uid 从url的链接里面来。
params.sec_uid = _utils.default.getUrlParam(window.location.href, "sec_uid"),
输入用户的分享url之后浏览器会跳转一个url。 参考这个博文

## max_cursor
一个时间戳，每次获得下商品列表的时候都会带上一个max_cursor 第一次请求是0

## signature
signature 是根据 页面中的uid 加密生成的
nonce = uid
signature = _bytedAcrawler.sign(nonce),
这个方法还用到了，页面全局的tac 
tac 可以直接在html代码中的一个script标签获取。

_bytedAcrawler 方法
```javascript
_bytedAcrawler = require("douyin_falcon:node_modules/byted-acrawler/dist/runtime")

```
`douyin_falcon:node_modules/byted-acrawler/dist/runtime`模块的定义
```javascript
;/*!douyin_falcon:node_modules/byted-acrawler/dist/runtime.js*/
__M.define("douyin_falcon:node_modules/byted-acrawler/dist/runtime", function(l, e) {
    Function(function(l) {
        return 'e(e,a,r){(b[e]||(b[e]=t("x,y","x "+e+" y")(r,a)}a(e,a,r){(k[r]||(k[r]=t("x,y","new x[y]("+Array(r+1).join(",x[y]")(1)+")")(e,a)}r(e,a,r){n,t,s={},b=s.d=r?r.d+1:0;for(s["$"+b]=s,t=0;t<b;t)s[n="$"+t]=r[n];for(t=0,b=s=a;t<b;t)s[t]=a[t];c(e,0,s)}c(t,b,k){u(e){v[x]=e}f{g=,ting(bg)}l{try{y=c(t,b,k)}catch(e){h=e,y=l}}for(h,y,d,g,v=[],x=0;;)switch(g=){case 1:u(!)4:f5:u((e){a=0,r=e;{c=a<r;c&&u(e[a]),c}}(6:y=,u((y8:if(g=,lg,g=,y===c)b+=g;else if(y!==l)y9:c10:u(s(11:y=,u(+y)12:for(y=f,d=[],g=0;g<y;g)d[g]=y.charCodeAt(g)^g+y;u(String.fromCharCode.apply(null,d13:y=,h=delete [y]14:59:u((g=)?(y=x,v.slice(x-=g,y:[])61:u([])62:g=,k[0]=65599*k[0]+k[1].charCodeAt(g)>>>065:h=,y=,[y]=h66:u(e(t[b],,67:y=,d=,u((g=).x===c?r(g.y,y,k):g.apply(d,y68:u(e((g=t[b])<"<"?(b--,f):g+g,,70:u(!1)71:n72:+f73:u(parseInt(f,3675:if(){bcase 74:g=<<16>>16g76:u(k[])77:y=,u([y])78:g=,u(a(v,x-=g+1,g79:g=,u(k["$"+g])81:h=,[f]=h82:u([f])83:h=,k[]=h84:!085:void 086:u(v[x-1])88:h=,y=,h,y89:u({e{r(e.y,arguments,k)}e.y=f,e.x=c,e})90:null91:h93:h=0:;default:u((g<<16>>16)-16)}}n=this,t=n.Function,s=Object.keys||(e){a={},r=0;for(c in e)a[r]=c;a=r,a},b={},k={};r'.replace(/[-]/g, function(e) {
            return l[15 & e.charCodeAt(0)]
        })
    }("v[x++]=v[--x]t.charCodeAt(b++)-32function return ))++.substrvar .length(),b+=;break;case ;break}".split("")))()('gr$Daten Иb/s!l y͒yĹg,(lfi~ah`{mv,-n|jqewVxp{rvmmx,&effkx[!cs"l".Pq%widthl"@q&heightl"vr*getContextx$"2d[!cs#l#,*;?|u.|uc{uq$fontl#vr(fillTextx$$龘ฑภ경2<[#c}l#2q*shadowBlurl#1q-shadowOffsetXl#$$limeq+shadowColorl#vr#arcx88802[%c}l#vr&strokex[ c}l"v,)}eOmyoZB]mx[ cs!0s$l$Pb<k7l l!r&lengthb%^l$1+s$jl  s#i$1ek1s$gr#tack4)zgr#tac$! +0o![#cj?o ]!l$b%s"o ]!l"l$b*b^0d#>>>s!0s%yA0s"l"l!r&lengthb<k+l"^l"1+s"jl  s&l&z0l!$ +["cs\'(0l#i\'1ps9wxb&s() &{s)/s(gr&Stringr,fromCharCodes)0s*yWl ._b&s o!])l l Jb<k$.aj;l .Tb<k$.gj/l .^b<k&i"-4j!+& s+yPo!]+s!l!l Hd>&l!l Bd>&+l!l <d>&+l!l 6d>&+l!l &+ s,y=o!o!]/q"13o!l q"10o!],l 2d>& s.{s-yMo!o!]0q"13o!]*Ld<l 4d#>>>b|s!o!l q"10o!],l!& s/yIo!o!].q"13o!],o!]*Jd<l 6d#>>>b|&o!]+l &+ s0l-l!&l-l!i\'1z141z4b/@d<l"b|&+l-l(l!b^&+l-l&zl\'g,)gk}ejo{cm,)|yn~Lij~em["cl$b%@d<l&zl\'l $ +["cl$b%b|&+l-l%8d<@b|l!b^&+ q$sign ', [Object.defineProperty(e, "__esModule", {
        value: !0
    })])
});
```
# dytk 
从请求url返回的html可以获取：
```javascript
(function() {
        $(function(){
            __M.require('douyin_falcon:page/reflow_user/index').init({
                uid: "110812020268",
                dytk: '5b2632429035ae972ca049e9414387e6'
            });
        });
    })();
```

## 短视频地址分析
一个视频的播放地址是：[https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fe10000bqnp6grd82dhhsqrppi0&ratio=720p&line=0](https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fe10000bqnp6grd82dhhsqrppi0&ratio=720p&line=0)

原视频无水印地址：[https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fe10000bqnp6grd82dhhsqrppi0&ratio=720p&line=0](https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fe10000bqnp6grd82dhhsqrppi0&ratio=720p&line=0)

ps:无水印版本的视频，需要在移动端环境打开，所以这里学要用移动端的请求头。

两个链接的区别是 无水印视频的url 从 `playwm` 变为 `play`

参考：[2020抖音无水印视频解析真实地址](https://blog.csdn.net/qq_36737934/article/details/104127835)

所以，接下来我们只需要根据之前获得的用户的视频列表数据，拼接出每个视频的下载地址即可。
