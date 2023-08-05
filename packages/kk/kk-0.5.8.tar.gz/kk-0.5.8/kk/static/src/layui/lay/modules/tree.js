/** layui-v2.5.6 MIT License By https://www.layui.com */
 ;layui.define("form",function(e){"use strict";var i=layui.$,a=layui.form,n=layui.layer,t="tree",r={config:{},index:layui[t]?layui[t].index+1e4:0,set:function(e){var a=this;return a.config=i.extend({},a.config,e),a},on:function(e,i){return layui.onevent.call(this,t,e,i)}},l=function(){var e=this,i=e.config,a=i.id||e.index;return l.that[a]=e,l.config[a]=i,{config:i,reload:function(i){e.reload.call(e,i)},getChecked:function(){return e.getChecked.call(e)},setChecked:function(i){return e.setChecked.call(e,i)}}},c="layui-hide",d="layui-disabled",s="layui-tree-set",o="layui-tree-iconClick",h="layui-icon-addition",u="layui-icon-subtraction",p="layui-tree-entry",f="layui-tree-main",y="layui-tree-txt",v="layui-tree-pack",C="layui-tree-spread",k="layui-tree-setLineShort",m="layui-tree-showLine",x="layui-tree-lineExtend",b=function(e){var a=this;a.index=++r.index,a.config=i.extend({},a.config,r.config,e),a.render()};b.prototype.config={data:[],showCheckbox:!1,showLine:!0,accordion:!1,onlyIconControl:!1,isJump:!1,edit:!1,text:{defaultNodeName:"未命名",none:"无数据"}},b.prototype.reload=function(e){var a=this;layui.each(e,function(e,i){i.constructor===Array&&delete a.config[e]}),a.config=i.extend(!0,{},a.config,e),a.render()},b.prototype.render=function(){var e=this,a=e.config;e.checkids=[];var n=i('<div class="layui-tree'+(a.showCheckbox?" layui-form":"")+(a.showLine?" layui-tree-line":"")+'" lay-filter="LAY-tree-'+e.index+'"></div>');e.tree(n);var t=a.elem=i(a.elem);if(t[0]){if(e.key=a.id||e.index,e.elem=n,e.elemNone=i('<div class="layui-tree-emptyText">'+a.text.none+"</div>"),t.html(e.elem),0==e.elem.find(".layui-tree-set").length)return e.elem.append(e.elemNone);a.showCheckbox&&e.renderForm("checkbox"),e.elem.find(".layui-tree-set").each(function(){var e=i(this);e.parent(".layui-tree-pack")[0]||e.addClass("layui-tree-setHide"),!e.next()[0]&&e.parents(".layui-tree-pack").eq(1).hasClass("layui-tree-lineExtend")&&e.addClass(k),e.next()[0]||e.parents(".layui-tree-set").eq(0).next()[0]||e.addClass(k)}),e.events()}},b.prototype.renderForm=function(e){a.render(e,"LAY-tree-"+this.index)},b.prototype.tree=function(e,a){var n=this,t=n.config,r=a||t.data;layui.each(r,function(a,r){var l=r.children&&r.children.length>0,o=i('<div class="layui-tree-pack" '+(r.spread?'style="display: block;"':"")+'"></div>'),h=i(['<div data-id="'+r.id+'" class="layui-tree-set'+(r.spread?" layui-tree-spread":"")+(r.checked?" layui-tree-checkedFirst":"")+'">','<div class="layui-tree-entry">','<div class="layui-tree-main">',function(){return t.showLine?l?'<span class="layui-tree-iconClick layui-tree-icon"><i class="layui-icon '+(r.spread?"layui-icon-subtraction":"layui-icon-addition")+'"></i></span>':'<span class="layui-tree-iconClick"><i class="layui-icon layui-icon-file"></i></span>':'<span class="layui-tree-iconClick"><i class="layui-tree-iconArrow '+(l?"":c)+'"></i></span>'}(),function(){return t.showCheckbox?'<input type="checkbox" name="'+(r.field||"layuiTreeCheck_"+r.id)+'" same="layuiTreeCheck" lay-skin="primary" '+(r.disabled?"disabled":"")+' value="'+r.id+'">':""}(),function(){return t.isJump&&r.href?'<a href="'+r.href+'" target="_blank" class="'+y+'">'+(r.title||r.label||t.text.defaultNodeName)+"</a>":'<span class="'+y+(r.disabled?" "+d:"")+'">'+(r.title||r.label||t.text.defaultNodeName)+"</span>"}(),"</div>",function(){if(!t.edit)return"";var e={add:'<i class="layui-icon layui-icon-add-1"  data-type="add"></i>',update:'<i class="layui-icon layui-icon-edit" data-type="update"></i>',del:'<i class="layui-icon layui-icon-delete" data-type="del"></i>'},i=['<div class="layui-btn-group layui-tree-btnGroup">'];return t.edit===!0&&(t.edit=["update","del"]),"object"==typeof t.edit?(layui.each(t.edit,function(a,n){i.push(e[n]||"")}),i.join("")+"</div>"):void 0}(),"</div></div>"].join(""));l&&(h.append(o),n.tree(o,r.children)),e.append(h),h.prev("."+s)[0]&&h.prev().children(".layui-tree-pack").addClass("layui-tree-showLine"),l||h.parent(".layui-tree-pack").addClass("layui-tree-lineExtend"),n.spread(h,r),t.showCheckbox&&(r.checked&&n.checkids.push(r.id),n.checkClick(h,r)),t.edit&&n.operate(h,r)})},b.prototype.spread=function(e,a){var n=this,t=n.config,r=e.children("."+p),l=r.children("."+f),c=r.find("."+o),k=r.find("."+y),m=t.onlyIconControl?c:l,x="";m.on("click",function(i){var a=e.children("."+v),n=m.children(".layui-icon")[0]?m.children(".layui-icon"):m.find(".layui-tree-icon").children(".layui-icon");if(a[0]){if(e.hasClass(C))e.removeClass(C),a.slideUp(200),n.removeClass(u).addClass(h);else if(e.addClass(C),a.slideDown(200),n.addClass(u).removeClass(h),t.accordion){var r=e.siblings("."+s);r.removeClass(C),r.children("."+v).slideUp(200),r.find(".layui-tree-icon").children(".layui-icon").removeClass(u).addClass(h)}}else x="normal"}),k.on("click",function(){var n=i(this);n.hasClass(d)||(x=e.hasClass(C)?t.onlyIconControl?"open":"close":t.onlyIconControl?"close":"open",t.click&&t.click({elem:e,state:x,data:a}))})},b.prototype.setCheckbox=function(e,i,a){var n=this,t=(n.config,a.prop("checked"));if(!a.prop("disabled")){if("object"==typeof i.children||e.find("."+v)[0]){var r=e.find("."+v).find('input[same="layuiTreeCheck"]');r.each(function(){this.disabled||(this.checked=t)})}var l=function(e){if(e.parents("."+s)[0]){var i,a=e.parent("."+v),n=a.parent(),r=a.prev().find('input[same="layuiTreeCheck"]');t?r.prop("checked",t):(a.find('input[same="layuiTreeCheck"]').each(function(){this.checked&&(i=!0)}),i||r.prop("checked",!1)),l(n)}};l(e),n.renderForm("checkbox")}},b.prototype.checkClick=function(e,a){var n=this,t=n.config,r=e.children("."+p),l=r.children("."+f);l.on("click",'input[same="layuiTreeCheck"]+',function(r){layui.stope(r);var l=i(this).prev(),c=l.prop("checked");l.prop("disabled")||(n.setCheckbox(e,a,l),t.oncheck&&t.oncheck({elem:e,checked:c,data:a}))})},b.prototype.operate=function(e,a){var t=this,r=t.config,l=e.children("."+p),d=l.children("."+f);l.children(".layui-tree-btnGroup").on("click",".layui-icon",function(l){layui.stope(l);var f=i(this).data("type"),b=e.children("."+v),g={data:a,type:f,elem:e};if("add"==f){b[0]||(r.showLine?(d.find("."+o).addClass("layui-tree-icon"),d.find("."+o).children(".layui-icon").addClass(h).removeClass("layui-icon-file")):d.find(".layui-tree-iconArrow").removeClass(c),e.append('<div class="layui-tree-pack"></div>'));var w=r.operate&&r.operate(g),N={};if(N.title=r.text.defaultNodeName,N.id=w,t.tree(e.children("."+v),[N]),r.showLine)if(b[0])b.hasClass(x)||b.addClass(x),e.find("."+v).each(function(){i(this).children("."+s).last().addClass(k)}),b.children("."+s).last().prev().hasClass(k)?b.children("."+s).last().prev().removeClass(k):b.children("."+s).last().removeClass(k),!e.parent("."+v)[0]&&e.next()[0]&&b.children("."+s).last().removeClass(k);else{var T=e.siblings("."+s),L=1,A=e.parent("."+v);layui.each(T,function(e,a){i(a).children("."+v)[0]||(L=0)}),1==L?(T.children("."+v).addClass(m),T.children("."+v).children("."+s).removeClass(k),e.children("."+v).addClass(m),A.removeClass(x),A.children("."+s).last().children("."+v).children("."+s).last().addClass(k)):e.children("."+v).children("."+s).addClass(k)}if(!r.showCheckbox)return;if(d.find('input[same="layuiTreeCheck"]')[0].checked){var I=e.children("."+v).children("."+s).last();I.find('input[same="layuiTreeCheck"]')[0].checked=!0}t.renderForm("checkbox")}else if("update"==f){var F=d.children("."+y).html();d.children("."+y).html(""),d.append('<input type="text" class="layui-tree-editInput">'),d.children(".layui-tree-editInput").val(F).focus();var j=function(e){var i=e.val().trim();i=i?i:r.text.defaultNodeName,e.remove(),d.children("."+y).html(i),g.data.title=i,r.operate&&r.operate(g)};d.children(".layui-tree-editInput").blur(function(){j(i(this))}),d.children(".layui-tree-editInput").on("keydown",function(e){13===e.keyCode&&(e.preventDefault(),j(i(this)))})}else n.confirm('确认删除该节点 "<span style="color: #999;">'+(a.title||"")+'</span>" 吗？',function(a){if(r.operate&&r.operate(g),g.status="remove",n.close(a),!e.prev("."+s)[0]&&!e.next("."+s)[0]&&!e.parent("."+v)[0])return e.remove(),void t.elem.append(t.elemNone);if(e.siblings("."+s).children("."+p)[0]){if(r.showCheckbox){var l=function(e){if(e.parents("."+s)[0]){var a=e.siblings("."+s).children("."+p),n=e.parent("."+v).prev(),r=n.find('input[same="layuiTreeCheck"]')[0],c=1,d=0;0==r.checked&&(a.each(function(e,a){var n=i(a).find('input[same="layuiTreeCheck"]')[0];0!=n.checked||n.disabled||(c=0),n.disabled||(d=1)}),1==c&&1==d&&(r.checked=!0,t.renderForm("checkbox"),l(n.parent("."+s))))}};l(e)}if(r.showLine){var d=e.siblings("."+s),h=1,f=e.parent("."+v);layui.each(d,function(e,a){i(a).children("."+v)[0]||(h=0)}),1==h?(b[0]||(f.removeClass(x),d.children("."+v).addClass(m),d.children("."+v).children("."+s).removeClass(k)),e.next()[0]?f.children("."+s).last().children("."+v).children("."+s).last().addClass(k):e.prev().children("."+v).children("."+s).last().addClass(k),e.next()[0]||e.parents("."+s)[1]||e.parents("."+s).eq(0).next()[0]||e.prev("."+s).addClass(k)):!e.next()[0]&&e.hasClass(k)&&e.prev().addClass(k)}}else{var y=e.parent("."+v).prev();if(r.showLine){y.find("."+o).removeClass("layui-tree-icon"),y.find("."+o).children(".layui-icon").removeClass(u).addClass("layui-icon-file");var w=y.parents("."+v).eq(0);w.addClass(x),w.children("."+s).each(function(){i(this).children("."+v).children("."+s).last().addClass(k)})}else y.find(".layui-tree-iconArrow").addClass(c);e.parents("."+s).eq(0).removeClass(C),e.parent("."+v).remove()}e.remove()})})},b.prototype.events=function(){var e=this,a=e.config;e.elem.find(".layui-tree-checkedFirst");e.setChecked(e.checkids),e.elem.find(".layui-tree-search").on("keyup",function(){var n=i(this),t=n.val(),r=n.nextAll(),l=[];r.find("."+y).each(function(){var e=i(this).parents("."+p);if(i(this).html().indexOf(t)!=-1){l.push(i(this).parent());var a=function(e){e.addClass("layui-tree-searchShow"),e.parent("."+v)[0]&&a(e.parent("."+v).parent("."+s))};a(e.parent("."+s))}}),r.find("."+p).each(function(){var e=i(this).parent("."+s);e.hasClass("layui-tree-searchShow")||e.addClass(c)}),0==r.find(".layui-tree-searchShow").length&&e.elem.append(e.elemNone),a.onsearch&&a.onsearch({elem:l})}),e.elem.find(".layui-tree-search").on("keydown",function(){i(this).nextAll().find("."+p).each(function(){var e=i(this).parent("."+s);e.removeClass("layui-tree-searchShow "+c)}),i(".layui-tree-emptyText")[0]&&i(".layui-tree-emptyText").remove()})},b.prototype.getChecked=function(){var e=this,a=e.config,n=[],t=[];e.elem.find(".layui-form-checked").each(function(){n.push(i(this).prev()[0].value)});var r=function(e,a){layui.each(e,function(e,t){layui.each(n,function(e,n){if(t.id==n){var l=i.extend({},t);return delete l.children,a.push(l),t.children&&(l.children=[],r(t.children,l.children)),!0}})})};return r(i.extend({},a.data),t),t},b.prototype.setChecked=function(e){var a=this;a.config;a.elem.find("."+s).each(function(a,n){var t=i(this).data("id"),r=i(n).children("."+p).find('input[same="layuiTreeCheck"]'),l=r.next();if("number"==typeof e){if(t==e)return r[0].checked||l.click(),!1}else"object"==typeof e&&layui.each(e,function(e,i){if(i==t&&!r[0].checked)return l.click(),!0})})},l.that={},l.config={},r.reload=function(e,i){var a=l.that[e];return a.reload(i),l.call(a)},r.getChecked=function(e){var i=l.that[e];return i.getChecked()},r.setChecked=function(e,i){var a=l.that[e];return a.setChecked(i)},r.render=function(e){var i=new b(e);return l.call(i)},e(t,r)});