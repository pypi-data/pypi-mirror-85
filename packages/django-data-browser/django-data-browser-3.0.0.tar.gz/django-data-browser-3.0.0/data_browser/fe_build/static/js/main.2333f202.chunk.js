(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{27:function(e,t,a){},51:function(e,t,a){e.exports=a(66)},56:function(e,t,a){},66:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(42),i=a.n(l),c=a(69),o=(a(56),a(7)),u=a(13),s=a(8),m=a(34),d=a(5),f=a(14),p=(a(27),a(28)),h=a(47),y=a(43),v=a(48),E=a(31),g=a.n(E),b=a(39),k=!1,F=void 0,S=document.getElementById("backend-version").textContent.trim();function j(e){var t=e.text,a=Object(n.useRef)(null);return r.a.createElement(r.a.Fragment,null,r.a.createElement("span",{ref:a},t)," ",r.a.createElement(O,{className:"CopyToClipboard",onClick:function(e){var t=document.createRange();t.selectNodeContents(a.current),window.getSelection().removeAllRanges(),window.getSelection().addRange(t),document.execCommand("copy"),window.getSelection().removeAllRanges(),e.target.blur()}},"(copy to clipboard)"))}function O(e){var t=e.className,a=e.onClick,n=e.children;return r.a.createElement("button",Object.assign({onClick:a},{type:"button",className:"Link "+(t||"")}),n)}function w(e){var t=e.className,a=e.onClick,n=e.children;return r.a.createElement("button",Object.assign({onClick:a},{type:"button",className:"sLink material-icons "+(t||"")}),n)}var N=function(e){Object(y.a)(a,e);var t=Object(h.a)(a);function a(){var e;Object(p.a)(this,a);for(var n=arguments.length,r=new Array(n),l=0;l<n;l++)r[l]=arguments[l];return(e=t.call.apply(t,[this].concat(r))).name="AbortError",e}return a}(Object(v.a)(Error));function C(e,t,a){return k?(F&&F.reject(new N("skipped")),new Promise((function(n,r){F={resolve:n,reject:r,url:e,options:t,process:a}}))):(k=!0,fetch(e,t).then((function(e){var t=F;if(F=void 0,k=!1,t)throw C(t.url,t.options,t.process).then((function(e){return t.resolve(e)}),(function(e){return t.reject(e)})),new N("superceeded");return e})).then((function(e){return b.ok(e.status>=200),b.ok(e.status<300),e})).then((function(e){var t=e.headers.get("x-version");return t!==S&&(console.log("Version mismatch, hard reload",S,t),window.location.reload(!0)),e})).then((function(e){return a(e)})))}function q(e){return C(e,{method:"GET"},(function(e){return e.json()}))}function L(e){var t=Object(n.useState)(),a=Object(u.a)(t,2),r=a[0],l=a[1];return Object(n.useEffect)((function(){q(e).then((function(e){return l(e)}))}),[e]),[r,function(t){l((function(e){return Object(o.a)({},e,{},t)})),function(e,t){return C(e,{method:"PATCH",headers:{"Content-Type":"application/json","X-CSRFToken":g.a.get("csrftoken")},body:JSON.stringify(t)},(function(e){return e.json()}))}(e,t).then((function(e){return l((function(t){return Object(o.a)({},t,{},e)}))})).catch((function(e){if("AbortError"!==e.name)throw e}))}]}function M(e){var t=e.name,a=e.apiUrl,l=e.data,i=e.redirectUrl,c=Object(n.useState)("save"),o=Object(u.a)(c,2),s=o[0],m=o[1];if("save"===s)return r.a.createElement(O,{onClick:function(e){m("saving"),function(e,t){return C(e,{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":g.a.get("csrftoken")},body:JSON.stringify(t)},(function(e){return e.json()}))}(a,l).then((function(e){return m(e)}))}},"Save ",t||"");if("saving"===s)return r.a.createElement(r.a.Fragment,null,"Saving ",t||"");var f="function"===typeof i?i(s):i;return r.a.createElement(d.a,{to:f})}function V(e){var t=e.name,a=e.apiUrl,l=e.redirectUrl,i=Object(n.useState)("normal"),c=Object(u.a)(i,2),o=c[0],s=c[1];if("normal"===o)return r.a.createElement(O,{onClick:function(e){s("confirm")}},"Delete ",t||"");if("confirm"===o)return r.a.createElement(O,{onClick:function(e){var t;s("deleting"),(t=a,C(t,{method:"DELETE",headers:{"X-CSRFToken":g.a.get("csrftoken")}},(function(e){return e}))).then((function(e){return s("deleted")}))}},"Are you sure?");if("deleting"===o)return"Deleting";if("deleted"===o)return r.a.createElement(d.a,{to:l});throw new Error("unknown delete state: ".concat(o))}function x(e){return e.message?r.a.createElement("div",{className:"Overlay"},r.a.createElement("h1",null,e.message)):null}Object.prototype.hasOwnProperty;var T=a(30);function U(e){var t=e.spaces;return t>0?Object(T.a)(Array(t)).map((function(e,t){return r.a.createElement("td",{className:"Empty",key:t})})):null}function _(e){var t=e.query,a=e.field,n=e.className,l=t.getField(a.pathStr),i=t.getType(l);return r.a.createElement("th",{className:n},r.a.createElement(w,{onClick:function(){return t.removeField(a)}},"close"),r.a.createElement(w,{onClick:function(){return t.moveField(a,!0)}},"chevron_left"),r.a.createElement(w,{onClick:function(){return t.moveField(a,!1)}},"chevron_right"),l.canPivot&&r.a.createElement(r.a.Fragment,null,r.a.createElement(w,{onClick:function(){return t.togglePivot(a)}},a.pivoted?"call_received":"call_made")),l.concrete&&i.defaultLookup?r.a.createElement(r.a.Fragment,null,r.a.createElement(w,{onClick:function(){return t.addFilter(a.pathStr)}},"filter_alt")," ",r.a.createElement(O,{onClick:function(){return t.toggleSort(a)}},t.prettyPathStr(a.pathStr),{dsc:"\u2191".concat(a.priority),asc:"\u2193".concat(a.priority),null:""}[a.sort])):" "+t.prettyPathStr(a.pathStr))}var P=r.a.memo((function(e){var t,a=e.modelField,n=e.className,l=e.span,i=e.value,c=e.formatHint;if(void 0===i)t="";else if(null===i)t=null;else if("html"===a.type&&i)t=r.a.createElement("div",{dangerouslySetInnerHTML:{__html:i}});else if("number"===a.type)if(i>c.highCutOff||i<-c.highCutOff||i&&i<c.lowCutOff&&i>-c.lowCutOff)t=i.toExponential(c.significantFigures-1);else{t=i.toFixed(c.decimalPlaces);var o=i.toFixed(c.decimalPlaces).toString().split(".");o[0]=o[0].replace(/\B(?=(\d{3})+(?!\d))/g,","),t=o.join(".")}else t=String(i);return r.a.createElement("td",{className:a.type+" "+n||"",colSpan:l||1},t)}));function H(e){var t=e.fields,a=e.query,n=e.classNameFirst,l=e.className;return t.map((function(e,t){return r.a.createElement(_,Object.assign({query:a,field:e},{key:e.pathStr,className:"HoriBorder ".concat(l," ")+(t?"":n)}))}))}function R(e){var t=e.fields,a=e.query,n=e.classNameFirst,l=e.className,i=e.row,c=e.formatHints;return t.map((function(e,t){return i?r.a.createElement(P,{key:e.pathStr,value:i[e.pathStr],className:"".concat(t?"":n," ").concat(l),modelField:a.getField(e.pathStr),formatHint:c[e.pathStr]}):r.a.createElement("td",{key:e.pathStr,className:"".concat(t?"":n," Empty")})}))}function A(e){var t=e.query,a=e.field,n=e.data,l=e.span,i=e.className,c=e.formatHints;return r.a.createElement(r.a.Fragment,null,r.a.createElement(_,{query:t,field:a}),n.map((function(e,n){return r.a.createElement(P,Object.assign({key:n,span:l,className:i},{value:e[a.pathStr],modelField:t.getField(a.pathStr),formatHint:c[a.pathStr]}))})))}function B(e){var t=e.query,a=e.cols,n=e.rows,l=e.body,i=e.overlay,c=e.formatHints;return r.a.createElement("div",{className:"Results"},r.a.createElement(x,{message:i}),r.a.createElement("div",{className:"Scroller"},r.a.createElement("table",null,r.a.createElement("thead",null,t.colFields().map((function(e){return r.a.createElement("tr",{key:e.pathStr},r.a.createElement(U,{spaces:t.rowFields().length-1}),r.a.createElement(A,Object.assign({query:t,field:e,formatHints:c},{span:t.resFields().length,data:a,className:i&&"Fade"})))})),r.a.createElement("tr",null,r.a.createElement(U,{spaces:1-t.rowFields().length}),r.a.createElement(H,Object.assign({query:t},{fields:t.rowFields(),className:"Freeze"})),a.map((function(e,a){return r.a.createElement(H,Object.assign({key:a,query:t},{fields:t.resFields(),classNameFirst:"LeftBorder",className:"Freeze"}))})))),r.a.createElement("tbody",{className:i&&"Fade"},n.map((function(e,a){return r.a.createElement("tr",{key:a},r.a.createElement(U,{spaces:1-t.rowFields().length}),r.a.createElement(R,Object.assign({query:t,row:e,formatHints:c},{fields:t.rowFields()})),l.map((function(e,n){return r.a.createElement(R,Object.assign({key:n,query:t,formatHints:c},{fields:t.resFields(),row:e[a],classNameFirst:"LeftBorder"}))})))}))))))}var D=a(37),I=a(45),Q={rows:[{}],cols:[{}],body:[[{}]],length:0,filterErrors:[],formatHints:{}};function J(e){return{model:e.model,fields:e.fields.map((function(e){return(e.pivoted?"&":"")+e.pathStr+{asc:"+".concat(e.priority),dsc:"-".concat(e.priority),null:""}[e.sort]})).join(","),query:e.filters.map((function(e){return"".concat(e.pathStr,"__").concat(e.lookup,"=").concat(e.value)})).join("&"),limit:e.limit}}function W(e,t){var a=J(e),n=a.model,r=a.fields,l=a.query,i=a.limit;return"query/".concat(n,"/").concat(r,".").concat(t,"?").concat(l,"&limit=").concat(i)}function X(e,t,a){var n=W(t,a);return"".concat(window.location.origin).concat(e).concat(n)}var z=function(){function e(t,a,n){Object(p.a)(this,e),this.config=t,this.query=a,this.setQuery=n}return Object(I.a)(e,[{key:"getField",value:function(e){var t,a=e.split("__"),n=this.query.model,r=Object(D.a)(a.slice(0,-1));try{for(r.s();!(t=r.n()).done;){var l=t.value;n=this.config.allModelFields[n].fields[l].model}}catch(i){r.e(i)}finally{r.f()}return this.config.allModelFields[n].fields[a.slice(-1)]}},{key:"getType",value:function(e){return this.config.types[e.type]}},{key:"getModelFields",value:function(e){return this.config.allModelFields[e]}},{key:"getDefaultLookupValue",value:function(e,t,a){var n=t.lookups[a].type;return n.endsWith("choice")?String(e.choices[0]):String(this.config.types[n].defaultValue)}},{key:"_getFieldIndex",value:function(e,t){return t.findIndex((function(t){return t.pathStr===e.pathStr}))}},{key:"addField",value:function(e,t){var a=this.query.fields.filter((function(t){return t.pathStr!==e})),n=a.map((function(e){return e.priority})).filter((function(e){return null!==e})),r=n.length?Math.max.apply(Math,Object(T.a)(n))+1:0;a.push({pathStr:e,sort:t,priority:t?r:null,pivoted:!1}),this.setQuery({fields:a})}},{key:"removeField",value:function(e){var t=this.getField(e.pathStr);this.setQuery({fields:this.query.fields.filter((function(t){return t.pathStr!==e.pathStr}))},t.canPivot)}},{key:"moveField",value:function(e,t){var a=this.getField(e.pathStr),n=this.colFields().slice(),r=this.rowFields().slice(),l=this.resFields().slice(),i=null;i=e.pivoted?n:a.canPivot||!n.length?r:l;var c=this._getFieldIndex(e,i),o=c+(t?-1:1);0<=o&&o<i.length&&(i.splice(c,1),i.splice(o,0,e),this.setQuery({fields:[].concat(r,n,l)},!1))}},{key:"toggleSort",value:function(e){var t=this._getFieldIndex(e,this.query.fields),a={asc:"dsc",dsc:null,null:"asc"}[e.sort],n=this.query.fields.slice();e.sort&&(n=n.map((function(t){return Object(o.a)({},t,{priority:null!=t.priority&&t.priority>e.priority?t.priority-1:t.priority})}))),a?(n=n.map((function(e){return Object(o.a)({},e,{priority:null!=e.priority?e.priority+1:e.priority})})))[t]=Object(o.a)({},e,{sort:a,priority:0}):n[t]=Object(o.a)({},e,{sort:null,priority:null}),this.setQuery({fields:n})}},{key:"togglePivot",value:function(e){var t=this._getFieldIndex(e,this.query.fields),a=this.query.fields.slice();a[t].pivoted=!a[t].pivoted,this.setQuery({fields:a})}},{key:"addFilter",value:function(e){var t=this.getField(e),a=this.getType(t),n=this.query.filters.slice();n.push({pathStr:e,lookup:a.defaultLookup,value:this.getDefaultLookupValue(t,a,a.defaultLookup)}),this.setQuery({filters:n})}},{key:"removeFilter",value:function(e){var t=this.query.filters.slice();t.splice(e,1),this.setQuery({filters:t})}},{key:"setFilterValue",value:function(e,t){var a=this.query.filters.slice();a[e]=Object(o.a)({},a[e],{value:t}),this.setQuery({filters:a})}},{key:"setFilterLookup",value:function(e,t){var a=this.query.filters.slice(),n=a[e],r=this.getField(a[e].pathStr),l=this.getType(r);l.lookups[n.lookup].type!==l.lookups[t].type&&(n.value=this.getDefaultLookupValue(r,l,t)),n.lookup=t,this.setQuery({filters:a})}},{key:"setLimit",value:function(e){e=Number(e),this.setQuery({limit:e>0?e:1})}},{key:"setModel",value:function(e){this.setQuery(Object(o.a)({model:e,fields:[],filters:this.config.allModelFields[e].defaultFilters,limit:this.config.defaultRowLimit},Q))}},{key:"getUrlForMedia",value:function(e){return X(this.config.baseUrl,this.query,e)}},{key:"colFields",value:function(){return this.query.fields.filter((function(e){return e.pivoted}))}},{key:"rowFields",value:function(){var e=this;return this.colFields().length?this.query.fields.filter((function(t){return!t.pivoted&&e.getField(t.pathStr).canPivot})):this.query.fields}},{key:"resFields",value:function(){var e=this;return this.colFields().length?this.query.fields.filter((function(t){return!e.getField(t.pathStr).canPivot})):[]}},{key:"prettyPathStr",value:function(e){var t,a=e.split("__"),n=[],r=this.query.model,l=null,i=Object(D.a)(a);try{for(i.s();!(t=i.n()).done;){var c=t.value;r=(l=this.config.allModelFields[r].fields[c]).model,n.push(l.prettyName)}}catch(o){i.e(o)}finally{i.f()}return n.join(" \u21d2 ")}}]),e}();function G(e){var t=e.lookup,a=e.lookupType,n=e.onChange,l=e.value,i=e.field,c=function(e){return n(e.target.value)};if("boolean"===e.lookup.type)return r.a.createElement("select",Object.assign({value:l},{onChange:c,className:"FilterValue"}),r.a.createElement("option",{value:!0},"true"),r.a.createElement("option",{value:!1},"false"));if("weekday"===t.type)return r.a.createElement("select",Object.assign({value:l},{onChange:c,className:"FilterValue"}),["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"].map((function(e){return r.a.createElement("option",{value:e},e)})));if("month"===t.type)return r.a.createElement("select",Object.assign({value:l},{onChange:c,className:"FilterValue"}),["January","Febuary","March","April","May","June","July","August","September","October","November","December"].map((function(e){return r.a.createElement("option",{value:e},e)})));if(a.choices.length)return r.a.createElement("select",Object.assign({value:l},{onChange:c,className:"FilterValue"}),a.choices.map((function(e){return r.a.createElement("option",{value:e},e)})));if(t.type.endsWith("choice"))return r.a.createElement("select",Object.assign({value:l},{onChange:c,className:"FilterValue"}),i.choices.map((function(e){return r.a.createElement("option",{value:e},e)})));if("number"===t.type||"numberchoice"===t.type||"year"===t.type)return r.a.createElement("input",Object.assign({value:l},{onChange:c,className:"FilterValue",type:"number",step:"0"}));if("jsonfield"===t.type){var o=l.split(/\|(.*)/);return r.a.createElement(r.a.Fragment,null,r.a.createElement("input",{value:o[0],onChange:function(e){return n("".concat(e.target.value,"|").concat(o[1]))},className:"FilterValue Half",type:"text"}),r.a.createElement("input",{value:o[1],onChange:function(e){return n("".concat(o[0],"|").concat(e.target.value))},className:"FilterValue Half",type:"text"}))}return r.a.createElement("input",Object.assign({value:l},{onChange:c,className:"FilterValue",type:"text"}))}function K(e){var t=e.pathStr,a=e.index,n=e.lookup,l=e.query,i=e.value,c=e.errorMessage,o=l.getField(t),u=l.getType(o);return r.a.createElement("tr",null,r.a.createElement("td",null,r.a.createElement(w,{onClick:function(){return l.removeFilter(a)}},"close")," ",r.a.createElement(O,{onClick:function(){return l.addField(t,u.defaultSort)}},l.prettyPathStr(t))," "),r.a.createElement("td",null,r.a.createElement("select",{className:"Lookup",value:n,onChange:function(e){return l.setFilterLookup(a,e.target.value)}},u.sortedLookups.map((function(e){return r.a.createElement("option",{key:e,value:e},e.replace(/_/g," "))})))),r.a.createElement("td",null,"="),r.a.createElement("td",null,r.a.createElement(G,Object.assign({value:i,field:o},{onChange:function(e){return l.setFilterValue(a,e)},lookup:u.lookups[n],lookupType:l.getType(u.lookups[n])})),c&&r.a.createElement("p",{className:"Error"},c)))}function Y(e){var t=e.query,a=e.filterErrors;return r.a.createElement("form",{className:"Filters"},r.a.createElement("table",{className:"Flat"},r.a.createElement("tbody",null,e.filters.map((function(e,n){return r.a.createElement(K,Object.assign({query:t,index:n},e,{key:n,errorMessage:a[n]}))})))))}function Z(e){var t=e.query,a=e.path,l=e.modelField,i=t.getType(l),c=Object(n.useState)(!1),o=Object(u.a)(c,2),s=o[0],m=o[1];return r.a.createElement(r.a.Fragment,null,r.a.createElement("tr",null,r.a.createElement("td",null,l.concrete&&i.defaultLookup&&r.a.createElement(w,{onClick:function(){return t.addFilter(a.join("__"))}},"filter_alt")),r.a.createElement("td",null,l.model&&r.a.createElement(w,{className:"ToggleLink",onClick:function(){return m((function(e){return!e}))}},s?"remove":"add")),r.a.createElement("td",null,l.type?r.a.createElement(O,{onClick:function(){return t.addField(a.join("__"),i.defaultSort)}},l.prettyName):l.prettyName)),s&&r.a.createElement("tr",null,r.a.createElement("td",null),r.a.createElement("td",{colSpan:"2"},r.a.createElement($,Object.assign({query:t,path:a},{model:l.model})))))}function $(e){var t=e.query,a=e.model,n=e.path,l=t.getModelFields(a);return r.a.createElement("table",null,r.a.createElement("tbody",null,l.sortedFields.map((function(e){var a=l.fields[e];return r.a.createElement(Z,Object.assign({key:e},{query:t,modelField:a},{path:n.concat([e])}))}))))}function ee(e){var t=e.query,a=e.sortedModels,n=e.model;return r.a.createElement("select",{className:"ModelSelector",onChange:function(e){return t.setModel(e.target.value)},value:n},a.map((function(e){return r.a.createElement("option",{key:e},e)})))}function te(e){return r.a.createElement(f.b,{to:"/",className:"Logo"},r.a.createElement("span",null,"DDB"),r.a.createElement("span",{className:"Version"},"v",S))}function ae(e){var t,a=e.query,n=e.rows,l=e.cols,i=e.body,c=e.length,o=e.sortedModels,u=e.model,s=e.filters,m=e.filterErrors,d=e.baseUrl,f=e.overlay,p=e.formatHints;return t=a.rowFields().length||a.colFields().length?r.a.createElement(B,{query:a,rows:n,cols:l,body:i,overlay:f,formatHints:p}):r.a.createElement("h2",null,"No fields selected"),r.a.createElement(r.a.Fragment,null,r.a.createElement(ee,{query:a,sortedModels:o,model:u}),r.a.createElement(Y,{query:a,filters:s,filterErrors:m}),r.a.createElement("p",null,r.a.createElement("span",{className:c>=a.query.limit?"Error":""},"Limit:"," ",r.a.createElement("input",{className:"RowLimit",type:"number",value:a.query.limit,onChange:function(e){a.setLimit(e.target.value)},min:"1"})," ","- Showing ",c," results -"," "),r.a.createElement("a",{href:a.getUrlForMedia("csv")},"Download as CSV")," -"," ",r.a.createElement("a",{href:a.getUrlForMedia("json")},"View as JSON")," -"," ",r.a.createElement(M,{name:"View",apiUrl:"".concat(d,"api/views/"),data:J(a.query),redirectUrl:function(e){return"/views/".concat(e.pk,".html")}})),r.a.createElement("div",{className:"MainSpace"},r.a.createElement("div",{className:"FieldsList"},r.a.createElement($,Object.assign({query:a,model:u},{path:[]}))),t,r.a.createElement("div",null)))}function ne(e){var t=e.canMakePublic,a=e.baseUrl,n=Object(d.h)().pk,l="".concat(a,"api/views/").concat(n,"/"),i=L(l),c=Object(u.a)(i,2),o=c[0],s=c[1];return o?r.a.createElement("div",{className:"EditSavedView"},r.a.createElement("div",{className:"SavedViewActions"},r.a.createElement("span",{className:"SavedViewTitle"},"Saved View"),r.a.createElement(f.b,{to:o.link},"Open")),r.a.createElement("form",null,r.a.createElement("input",{type:"text",value:o.name,onChange:function(e){s({name:e.target.value})},className:"SavedViewName",placeholder:"enter a name"}),r.a.createElement("table",null,r.a.createElement("tbody",null,r.a.createElement("tr",null,r.a.createElement("th",null,"Model:"),r.a.createElement("td",null,o.model)),r.a.createElement("tr",null,r.a.createElement("th",null,"Fields:"),r.a.createElement("td",null,o.fields.replace(/,/g,"\u200b,"))),r.a.createElement("tr",null,r.a.createElement("th",null,"Filters:"),r.a.createElement("td",null,o.query.replace(/&/g,"\u200b&"))),r.a.createElement("tr",null,r.a.createElement("th",null,"Limit:"),r.a.createElement("td",{className:"SavedViewLimit"},r.a.createElement("input",{className:"RowLimit",type:"number",value:o.limit,onChange:function(e){s({limit:e.target.value})}}))),r.a.createElement("tr",null,r.a.createElement("th",null,"Created Time:"),r.a.createElement("td",null,o.createdTime)))),r.a.createElement("textarea",{value:o.description,onChange:function(e){s({description:e.target.value})},placeholder:"enter a description"}),t&&r.a.createElement("table",null,r.a.createElement("tbody",null,r.a.createElement("tr",null,r.a.createElement("th",null,"Is Public:"),r.a.createElement("td",null,r.a.createElement("input",{type:"checkbox",checked:o.public,onChange:function(e){s({public:e.target.checked})}}))),r.a.createElement("tr",null,r.a.createElement("th",null,"Public link:"),r.a.createElement("td",null,o.public&&r.a.createElement(j,{text:o.publicLink}))),r.a.createElement("tr",null,r.a.createElement("th",null,"Google Sheets:"),r.a.createElement("td",null,o.public&&r.a.createElement(j,{text:o.googleSheetsFormula})))))),r.a.createElement("div",{className:"SavedViewActions"},r.a.createElement(V,{apiUrl:l,redirectUrl:"/"}),r.a.createElement(f.b,{to:"/"},"Done"))):""}function re(e){var t=e.baseUrl,a=L("".concat(t,"api/views/")),n=Object(u.a)(a,1)[0];return n?r.a.createElement("div",null,r.a.createElement("h1",null,"Saved Views"),r.a.createElement("div",null,n.map((function(e,t){return r.a.createElement("div",{key:t},r.a.createElement("p",null,r.a.createElement(f.b,{className:"Link",to:e.link},e.name," - ",e.model)," ","(",r.a.createElement(f.b,{to:"/views/".concat(e.pk,".html")},"edit"),")"),r.a.createElement("p",null,e.description))})))):""}function le(e){var t=e.sortedModels,a=e.baseUrl,n=e.defaultRowLimit,l=e.allModelFields;return r.a.createElement("div",{className:"Index"},r.a.createElement("div",null,r.a.createElement("h1",null,"Models"),r.a.createElement("div",null,t.map((function(e){return r.a.createElement("div",{key:e},r.a.createElement(f.b,{to:W({model:e,fields:[],filters:l[e].defaultFilters,limit:n},"html"),className:"Link"},e))})))),r.a.createElement(re,{baseUrl:a}))}var ie=a(39);function ce(e){var t=e.config,a=Object(d.h)(),l=a.model,i=a.fieldStr,c=Object(n.useState)("Booting..."),f=Object(u.a)(c,2),p=f[0],h=f[1],y=Object(n.useState)(Object(o.a)({model:"",fields:[],filters:[],limit:t.defaultRowLimit},Q)),v=Object(u.a)(y,2),E=v[0],g=v[1],b=Object(d.g)().search,F=function(e){"AbortError"!==e.name&&(h("Error"),console.log(e),s.a(e))},S=function(e){return h("Loading..."),q(X(t.baseUrl,e,"json")).then((function(e){return g((function(t){return Object(o.a)({},t,{body:e.body,cols:e.cols,rows:e.rows,length:e.length,formatHints:e.formatHints,filterErrors:e.filterErrors})})),h(k?"Loading...":void 0),e}))};Object(n.useEffect)((function(){var e=function(e){g(e.state),S(e.state).catch(F)};return q("".concat(t.baseUrl,"query/").concat(l,"/").concat(i||"",".query").concat(b)).then((function(a){var n=Object(o.a)({model:a.model,fields:a.fields,filters:a.filters,limit:a.limit},Q);g(n),h("Loading..."),window.history.replaceState(n,null,X(t.baseUrl,n,"html")),window.addEventListener("popstate",e),S(n).catch(F)})),function(){window.removeEventListener("popstate",e)}}),[]);if("Booting..."===p)return"";var j=new z(t,E,(function(e){var a=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],n=Object(o.a)({},E,{},e);g(n);var r=Object(o.a)({model:n.model,fields:n.fields,filters:n.filters,limit:n.limit},Q);window.history.pushState(r,null,X(t.baseUrl,n,"html")),a&&S(n).then((function(e){var t=Object(o.a)({},e,{},Q);t.filters=Object(m.sortBy)(t.filters,["pathStr"]);var a=Object(o.a)({},r);a.filters=Object(m.sortBy)(a.filters,["pathStr"]),ie.deepStrictEqual(t,a)})).catch(F)}));return r.a.createElement(ae,Object.assign({overlay:p,query:j,sortedModels:t.sortedModels,baseUrl:t.baseUrl},E))}var oe=function(e){var t=e.baseUrl,a=e.canMakePublic;return r.a.createElement(f.a,{basename:t},r.a.createElement(te,null),r.a.createElement("div",{id:"body"},r.a.createElement(d.d,null,r.a.createElement(d.b,{path:"/query/:model/:fieldStr?.html"},r.a.createElement(ce,{config:e})),r.a.createElement(d.b,{path:"/views/:pk.html"},r.a.createElement(ne,{baseUrl:t,canMakePublic:a})),r.a.createElement(d.b,{path:"/"},r.a.createElement(le,e)))))},ue=JSON.parse(document.getElementById("backend-config").textContent),se=document.getElementById("backend-version").textContent.trim();ue.sentryDsn&&c.a({dsn:ue.sentryDsn,release:se,attachStacktrace:!0,maxValueLength:1e4}),i.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(oe,ue)),document.getElementById("root"))}},[[51,1,2]]]);
//# sourceMappingURL=main.2333f202.chunk.js.map