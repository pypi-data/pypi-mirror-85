/*! For license information please see chunk.b54f5e5d36885556ecd8.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3001],{91107:(t,a,p)=>{"use strict";p.d(a,{Ud:()=>m});const e=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),r=Symbol("Comlink.releaseProxy"),n=Symbol("Comlink.thrown"),i=t=>"object"==typeof t&&null!==t||"function"==typeof t,d=new Map([["proxy",{canHandle:t=>i(t)&&t[e],serialize(t){const{port1:a,port2:p}=new MessageChannel;return c(t,a),[p,[p]]},deserialize:t=>(t.start(),m(t))}],["throw",{canHandle:t=>i(t)&&n in t,serialize({value:t}){let a;return a=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[a,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function c(t,a=self){a.addEventListener("message",(function p(o){if(!o||!o.data)return;const{id:r,type:i,path:d}=Object.assign({path:[]},o.data),m=(o.data.argumentList||[]).map(u);let l;try{const a=d.slice(0,-1).reduce(((t,a)=>t[a]),t),p=d.reduce(((t,a)=>t[a]),t);switch(i){case 0:l=p;break;case 1:a[d.slice(-1)[0]]=u(o.data.value),l=!0;break;case 2:l=p.apply(a,m);break;case 3:l=function(t){return Object.assign(t,{[e]:!0})}(new p(...m));break;case 4:{const{port1:a,port2:p}=new MessageChannel;c(t,p),l=function(t,a){return h.set(t,a),t}(a,[a])}break;case 5:l=void 0}}catch(b){l={value:b,[n]:0}}Promise.resolve(l).catch((t=>({value:t,[n]:0}))).then((t=>{const[e,o]=f(t);a.postMessage(Object.assign(Object.assign({},e),{id:r}),o),5===i&&(a.removeEventListener("message",p),s(a))}))})),a.start&&a.start()}function s(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function m(t,a){return b(t,[],a)}function l(t){if(t)throw new Error("Proxy has been released and is not useable")}function b(t,a=[],p=function(){}){let e=!1;const n=new Proxy(p,{get(p,o){if(l(e),o===r)return()=>_(t,{type:5,path:a.map((t=>t.toString()))}).then((()=>{s(t),e=!0}));if("then"===o){if(0===a.length)return{then:()=>n};const p=_(t,{type:0,path:a.map((t=>t.toString()))}).then(u);return p.then.bind(p)}return b(t,[...a,o])},set(p,o,r){l(e);const[n,i]=f(r);return _(t,{type:1,path:[...a,o].map((t=>t.toString())),value:n},i).then(u)},apply(p,r,n){l(e);const i=a[a.length-1];if(i===o)return _(t,{type:4}).then(u);if("bind"===i)return b(t,a.slice(0,-1));const[d,c]=g(n);return _(t,{type:2,path:a.map((t=>t.toString())),argumentList:d},c).then(u)},construct(p,o){l(e);const[r,n]=g(o);return _(t,{type:3,path:a.map((t=>t.toString())),argumentList:r},n).then(u)}});return n}function g(t){const a=t.map(f);return[a.map((t=>t[0])),(p=a.map((t=>t[1])),Array.prototype.concat.apply([],p))];var p}const h=new WeakMap;function f(t){for(const[a,p]of d)if(p.canHandle(t)){const[e,o]=p.serialize(t);return[{type:3,name:a,value:e},o]}return[{type:0,value:t},h.get(t)||[]]}function u(t){switch(t.type){case 3:return d.get(t.name).deserialize(t.value);case 0:return t.value}}function _(t,a,p){return new Promise((e=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function a(p){p.data&&p.data.id&&p.data.id===o&&(t.removeEventListener("message",a),e(p.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:o},a),p)}))}},3239:(t,a,p)=>{"use strict";function e(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(e);var a={};return Object.keys(t).forEach((function(p){a[p]=e(t[p])})),a}p.d(a,{Z:()=>e})},16861:(t,a,p)=>{"use strict";p.d(a,{F:()=>n});var e=p(37581),o=p(94707);const r=new WeakMap,n=(0,o.XM)((t=>a=>{if(!(a instanceof o.nt))throw new Error("cache can only be used in text bindings");let p=r.get(a);void 0===p&&(p=new WeakMap,r.set(a,p));const n=a.value;if(n instanceof e.R){if(t instanceof o.js&&n.template===a.options.templateFactory(t))return void a.setValue(t);{let t=p.get(n.template);void 0===t&&(t={instance:n,nodes:document.createDocumentFragment()},p.set(n.template,t)),(0,o.V)(t.nodes,a.startNode.nextSibling,a.endNode)}}if(t instanceof o.js){const e=a.options.templateFactory(t),o=p.get(e);void 0!==o&&(a.setValue(o.nodes),a.commit(),a.value=o.instance)}a.setValue(t)}))},23049:(t,a,p)=>{"use strict";p.d(a,{Z:()=>e});const e="/**\n * @license\n * Copyright Google LLC All Rights Reserved.\n *\n * Use of this source code is governed by an MIT-style license that can be\n * found in the LICENSE file at https://github.com/material-components/material-components-web/blob/master/LICENSE\n */\n.mdc-top-app-bar{background-color:#6200ee;background-color:var(--mdc-theme-primary, #6200ee);color:white;display:flex;position:fixed;flex-direction:column;justify-content:space-between;box-sizing:border-box;width:100%;z-index:4}.mdc-top-app-bar .mdc-top-app-bar__action-item,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon{color:#fff;color:var(--mdc-theme-on-primary, #fff)}.mdc-top-app-bar .mdc-top-app-bar__action-item::before,.mdc-top-app-bar .mdc-top-app-bar__action-item::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::after{background-color:#fff;background-color:var(--mdc-theme-on-primary, #fff)}.mdc-top-app-bar .mdc-top-app-bar__action-item:hover::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:hover::before{opacity:.08}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):focus::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.24}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded)::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):active::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.24}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.24}.mdc-top-app-bar__row{display:flex;position:relative;box-sizing:border-box;width:100%;height:64px}.mdc-top-app-bar__section{display:inline-flex;flex:1 1 auto;align-items:center;min-width:0;padding:8px 12px;z-index:1}.mdc-top-app-bar__section--align-start{justify-content:flex-start;order:-1}.mdc-top-app-bar__section--align-end{justify-content:flex-end;order:1}.mdc-top-app-bar__title{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-headline6-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1.25rem;font-size:var(--mdc-typography-headline6-font-size, 1.25rem);line-height:2rem;line-height:var(--mdc-typography-headline6-line-height, 2rem);font-weight:500;font-weight:var(--mdc-typography-headline6-font-weight, 500);letter-spacing:0.0125em;letter-spacing:var(--mdc-typography-headline6-letter-spacing, 0.0125em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-headline6-text-transform, inherit);padding-left:20px;padding-right:0;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;z-index:1}[dir=rtl] .mdc-top-app-bar__title,.mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--short-collapsed{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:24px;border-bottom-left-radius:0}[dir=rtl] .mdc-top-app-bar--short-collapsed,.mdc-top-app-bar--short-collapsed[dir=rtl]{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:0;border-bottom-left-radius:24px}.mdc-top-app-bar--short{top:0;right:auto;left:0;width:100%;transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-top-app-bar--short,.mdc-top-app-bar--short[dir=rtl]{right:0;left:auto}.mdc-top-app-bar--short .mdc-top-app-bar__row{height:56px}.mdc-top-app-bar--short .mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short .mdc-top-app-bar__title{transition:opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);opacity:1}.mdc-top-app-bar--short-collapsed{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);width:56px;transition:width 300ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__title{display:none}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__action-item{transition:padding 150ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item{width:112px}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--dense .mdc-top-app-bar__row{height:48px}.mdc-top-app-bar--dense .mdc-top-app-bar__section{padding:0 4px}.mdc-top-app-bar--dense .mdc-top-app-bar__title{padding-left:12px;padding-right:0}[dir=rtl] .mdc-top-app-bar--dense .mdc-top-app-bar__title,.mdc-top-app-bar--dense .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:12px}.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:128px}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{align-self:flex-end;padding-bottom:2px}.mdc-top-app-bar--prominent .mdc-top-app-bar__action-item,.mdc-top-app-bar--prominent .mdc-top-app-bar__navigation-icon{align-self:flex-start}.mdc-top-app-bar--fixed{transition:box-shadow 200ms linear}.mdc-top-app-bar--fixed-scrolled{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);transition:box-shadow 200ms linear}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:96px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__section{padding:0 12px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-left:20px;padding-right:0;padding-bottom:9px}[dir=rtl] .mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title,.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--fixed-adjust{padding-top:64px}.mdc-top-app-bar--dense-fixed-adjust{padding-top:48px}.mdc-top-app-bar--short-fixed-adjust{padding-top:56px}.mdc-top-app-bar--prominent-fixed-adjust{padding-top:128px}.mdc-top-app-bar--dense-prominent-fixed-adjust{padding-top:96px}@media(max-width: 599px){.mdc-top-app-bar__row{height:56px}.mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short{transition:width 200ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed{transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-bottom:6px}.mdc-top-app-bar--fixed-adjust{padding-top:56px}}\n\n/*# sourceMappingURL=mdc.top-app-bar.min.css.map*/"}}]);
//# sourceMappingURL=chunk.b54f5e5d36885556ecd8.js.map