/*! For license information please see chunk.9bc3dc3319763c6b9bbe.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[469],{99257:(e,t,i)=>{"use strict";i(43437);var r=i(15112),n=i(9672),o=i(87156);(0,n.k)({is:"iron-iconset-svg",properties:{name:{type:String,observer:"_nameChanged"},size:{type:Number,value:24},rtlMirroring:{type:Boolean,value:!1},useGlobalRtlAttribute:{type:Boolean,value:!1}},created:function(){this._meta=new r.P({type:"iconset",key:null,value:null})},attached:function(){this.style.display="none"},getIconNames:function(){return this._icons=this._createIconMap(),Object.keys(this._icons).map((function(e){return this.name+":"+e}),this)},applyIcon:function(e,t){this.removeIcon(e);var i=this._cloneIcon(t,this.rtlMirroring&&this._targetIsRTL(e));if(i){var r=(0,o.vz)(e.root||e);return r.insertBefore(i,r.childNodes[0]),e._svgIcon=i}return null},removeIcon:function(e){e._svgIcon&&((0,o.vz)(e.root||e).removeChild(e._svgIcon),e._svgIcon=null)},_targetIsRTL:function(e){if(null==this.__targetIsRTL)if(this.useGlobalRtlAttribute){var t=document.body&&document.body.hasAttribute("dir")?document.body:document.documentElement;this.__targetIsRTL="rtl"===t.getAttribute("dir")}else e&&e.nodeType!==Node.ELEMENT_NODE&&(e=e.host),this.__targetIsRTL=e&&"rtl"===window.getComputedStyle(e).direction;return this.__targetIsRTL},_nameChanged:function(){this._meta.value=null,this._meta.key=this.name,this._meta.value=this,this.async((function(){this.fire("iron-iconset-added",this,{node:window})}))},_createIconMap:function(){var e=Object.create(null);return(0,o.vz)(this).querySelectorAll("[id]").forEach((function(t){e[t.id]=t})),e},_cloneIcon:function(e,t){return this._icons=this._icons||this._createIconMap(),this._prepareSvgClone(this._icons[e],this.size,t)},_prepareSvgClone:function(e,t,i){if(e){var r=e.cloneNode(!0),n=document.createElementNS("http://www.w3.org/2000/svg","svg"),o=r.getAttribute("viewBox")||"0 0 "+t+" "+t,s="pointer-events: none; display: block; width: 100%; height: 100%;";return i&&r.hasAttribute("mirror-in-rtl")&&(s+="-webkit-transform:scale(-1,1);transform:scale(-1,1);transform-origin:center;"),n.setAttribute("viewBox",o),n.setAttribute("preserveAspectRatio","xMidYMid meet"),n.setAttribute("focusable","false"),n.style.cssText=s,n.appendChild(r).removeAttribute("id"),n}return null}})},60461:e=>{e.exports=function e(t){return Object.freeze(t),Object.getOwnPropertyNames(t).forEach((function(i){!t.hasOwnProperty(i)||null===t[i]||"object"!=typeof t[i]&&"function"!=typeof t[i]||Object.isFrozen(t[i])||e(t[i])})),t}},7323:(e,t,i)=>{"use strict";i.d(t,{p:()=>r});const r=(e,t)=>e&&-1!==e.config.components.indexOf(t)},69470:(e,t,i)=>{"use strict";i.d(t,{j:()=>n,fs:()=>o,$y:()=>s});const r=(e,t,i)=>new Promise(((r,n)=>{const o=document.createElement(e);let s="src",a="body";switch(o.onload=()=>r(t),o.onerror=()=>n(t),e){case"script":o.async=!0,i&&(o.type=i);break;case"link":o.type="text/css",o.rel="stylesheet",s="href",a="head"}o[s]=t,document[a].appendChild(o)})),n=e=>r("link",e),o=e=>r("script",e),s=e=>r("script",e,"module")},86977:(e,t,i)=>{"use strict";i.d(t,{Q:()=>r});const r=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},11950:(e,t,i)=>{"use strict";i.d(t,{l:()=>r});const r=async(e,t)=>new Promise((i=>{const r=t(e,(e=>{r(),i(e)}))}))},81545:(e,t,i)=>{"use strict";i(53918),i(29290);var r=i(15652);i(10983);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function o(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var c=n();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,u.elements)}),i),u=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(l(o.descriptor)||l(n.descriptor)){if(a(o)||a(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(a(o)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(h.d.map(o)),e);c.initializeClassElements(h.F,u.elements),c.runClassFinishers(h.F,u.finishers)}([(0,r.Mo)("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return r.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),r.oi)},46167:(e,t,i)=>{"use strict";i(87482);var r=i(15652);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function o(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function u(e,t,i){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const f=customElements.get("paper-tabs");let m;!function(e,t,i,r){var c=n();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,u.elements)}),i),u=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(l(o.descriptor)||l(n.descriptor)){if(a(o)||a(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(a(o)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(h.d.map(o)),e);c.initializeClassElements(h.F,u.elements),c.runClassFinishers(h.F,u.finishers)}([(0,r.Mo)("ha-tabs")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"_firstTabWidth",value:()=>0},{kind:"field",key:"_lastTabWidth",value:()=>0},{kind:"field",key:"_lastLeftHiddenState",value:()=>!1},{kind:"get",static:!0,key:"template",value:function(){if(!m){m=f.template.cloneNode(!0);const e=m.content.querySelector("style");m.content.querySelectorAll("paper-icon-button").forEach((e=>{e.setAttribute("noink","")})),e.appendChild(document.createTextNode("\n          :host {\n            padding-top: .5px;\n          }\n          .not-visible {\n            display: none;\n          }\n          paper-icon-button {\n            width: 24px;\n            height: 48px;\n            padding: 0;\n            margin: 0;\n          }\n        "))}return m}},{kind:"method",key:"_tabChanged",value:function(e,t){u(p(i.prototype),"_tabChanged",this).call(this,e,t);const r=this.querySelectorAll("paper-tab:not(.hide-tab)");r.length>0&&(this._firstTabWidth=r[0].clientWidth,this._lastTabWidth=r[r.length-1].clientWidth);const n=this.querySelector(".iron-selected");n&&n.scrollIntoView()}},{kind:"method",key:"_affectScroll",value:function(e){if(0===this._firstTabWidth||0===this._lastTabWidth)return;this.$.tabsContainer.scrollLeft+=e;const t=this.$.tabsContainer.scrollLeft;this._leftHidden=t-this._firstTabWidth<0,this._rightHidden=t+this._lastTabWidth>this._tabContainerScrollSize,this._lastLeftHiddenState!==this._leftHidden&&(this._lastLeftHiddenState=this._leftHidden,this.$.tabsContainer.scrollLeft+=this._leftHidden?-23:23)}}]}}),f)},57066:(e,t,i)=>{"use strict";i.d(t,{Lo:()=>s,IO:()=>a,qv:()=>l,sG:()=>h});var r=i(95282),n=i(85415),o=i(38346);const s=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),a=(e,t,i)=>e.callWS({type:"config/area_registry/update",area_id:t,...i}),l=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),c=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,t)=>(0,n.q)(e.name,t.name))))),d=(e,t)=>e.subscribeEvents((0,o.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"area_registry_updated"),h=(e,t)=>(0,r.B)("_areaRegistry",c,d,e,t)},74186:(e,t,i)=>{"use strict";i.d(t,{eD:()=>s,Mw:()=>a,vA:()=>l,L3:()=>c,Nv:()=>d,z3:()=>h,LM:()=>f});var r=i(95282),n=i(91741),o=i(38346);const s=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class)),a=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class)),l=(e,t)=>{if(t.name)return t.name;const i=e.states[t.entity_id];return i?(0,n.C)(i):null},c=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t,i)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...i}),h=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),u=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),p=(e,t)=>e.subscribeEvents((0,o.D)((()=>u(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),f=(e,t)=>(0,r.B)("_entityRegistry",u,p,e,t)},15327:(e,t,i)=>{"use strict";i.d(t,{eL:()=>r,SN:()=>n,id:()=>o,fg:()=>s,j2:()=>a,JR:()=>l,Y:()=>c,iM:()=>d,Q2:()=>h,Oh:()=>u,vj:()=>p,Gc:()=>f});const r=e=>e.sendMessagePromise({type:"lovelace/resources"}),n=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),o=(e,t,i)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...i}),s=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),a=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),c=(e,t,i)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...i}),d=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),h=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i}),u=(e,t,i)=>e.callWS({type:"lovelace/config/save",url_path:t,config:i}),p=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),f=(e,t,i)=>e.subscribeEvents((e=>{e.data.url_path===t&&i()}),"lovelace_updated")},51444:(e,t,i)=>{"use strict";i.d(t,{_:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(5009),i.e(1199),i.e(7033)]).then(i.bind(i,72420)),o=e=>{(0,r.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:n,dialogParams:{}})}},27849:(e,t,i)=>{"use strict";i(39841);var r=i(50856);i(28426);class n extends(customElements.get("app-header-layout")){static get template(){return r.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",n)},17852:(e,t,i)=>{"use strict";i.d(t,{VG:()=>k,UO:()=>P});var r=i(4915),n=i(58831),o=i(27269),s=i(22311),a=i(91741),l=i(49706);var c=i(85415),d=i(11950),h=i(57066),u=i(57292),p=i(74186),f=i(5986),m=i(41499),v=i(14748);const y=["binary_sensor","mailbox","person","sensor","sun","timer"],g=new Set(["automation","configurator","device_tracker","geo_location","persistent_notification","zone"]),w=new Set(["mobile_app"]);let b=!1;const k=(e,t,i=!1)=>{const r=[],o=[],s=t.title?t.title+" ":void 0;for(const[l,c]of e){const e=(0,n.M)(l);if("alarm_control_panel"===e){const e={type:"alarm-panel",entity:l};r.push(e)}else if("camera"===e){const e={type:"picture-entity",entity:l};r.push(e)}else if("climate"===e){const e={type:"thermostat",entity:l};r.push(e)}else if("humidifier"===e){const e={type:"humidifier",entity:l};r.push(e)}else if("light"===e&&i){const e={type:"light",entity:l};r.push(e)}else if("media_player"===e){const e={type:"media-control",entity:l};r.push(e)}else if("plant"===e){const e={type:"plant-status",entity:l};r.push(e)}else if("weather"===e){const e={type:"weather-forecast",entity:l,show_forecast:!1};r.push(e)}else if("sensor"===e&&(null==c?void 0:c.attributes.device_class)===m.A);else{let e;const t=s&&c&&(e=(0,a.C)(c)).startsWith(s)?{entity:l,name:e.substr(s.length)}:l;o.push(t)}}return o.length>0&&r.unshift({type:"entities",entities:o,...t}),r},_=(e,t,i,r,o,l)=>{const d=(e=>{const t=[],i={};return Object.keys(e).forEach((r=>{const o=e[r];"group"===(0,n.M)(r)?t.push(o):i[r]=o})),t.forEach((e=>e.attributes.entity_id.forEach((e=>{delete i[e]})))),{groups:t,ungrouped:i}})(o);d.groups.sort(((e,t)=>l[e.entity_id]-l[t.entity_id]));const h={},u={};Object.keys(d.ungrouped).forEach((e=>{const t=d.ungrouped[e],i=(0,s.N)(t),r=y.includes(i)?h:u;i in r||(r[i]=[]),r[i].push(t.entity_id)}));let p=[];y.forEach((e=>{e in h&&(p=p.concat(h[e]))}));let m=[];d.groups.forEach((e=>{m=m.concat(k(e.attributes.entity_id.map((e=>[e,o[e]])),{title:(0,a.C)(e),show_header_toggle:"hidden"!==e.attributes.control}))})),Object.keys(u).sort().forEach((t=>{m=m.concat(k(u[t].sort(((e,t)=>(0,c.q)((0,a.C)(o[e]),(0,a.C)(o[t])))).map((e=>[e,o[e]])),{title:(0,f.Lh)(e,t)}))}));const g={path:t,title:i,badges:(0,v.Q)(p),cards:m};return r&&(g.icon=r),g},E=(e,t,i,r,n)=>{const o=((e,t)=>{const i={},r=new Set(t.filter((e=>w.has(e.platform))).map((e=>e.entity_id)));return Object.keys(e).forEach((t=>{const n=e[t];g.has((0,s.N)(n))||r.has(n.entity_id)||(i[t]=e[t])})),i})(r,i),a={};Object.keys(o).forEach((e=>{const t=o[e];t.attributes.order&&(a[e]=t.attributes.order)}));const l=((e,t,i,r)=>{const n={...r},o=[];for(const s of e){const e=[],r=new Set(t.filter((e=>e.area_id===s.area_id)).map((e=>e.id)));for(const t of i)r.has(t.device_id)&&t.entity_id in n&&(e.push(n[t.entity_id]),delete n[t.entity_id]);e.length>0&&o.push([s,e])}return{areasWithEntities:o,otherEntities:n}})(e,t,i,o),c=_(n,"default_view","Home",undefined,l.otherEntities,a),d=[];return l.areasWithEntities.forEach((([e,t])=>{d.push(...k(t.map((e=>[e.entity_id,e])),{title:e.name}))})),c.cards.unshift(...d),c},C=async(e,t,i,r,s,c)=>{if(e.safe_mode)return{title:e.location_name,views:[{cards:[{type:"safe-mode"}]}]};const d=(e=>{const t=[];return Object.keys(e).forEach((i=>{const r=e[i];r.attributes.view&&t.push(r)})),t.sort(((e,t)=>e.entity_id===l.a1?-1:t.entity_id===l.a1?1:e.attributes.order-t.attributes.order)),t})(s),h=d.map((e=>{const t=((e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const r=e[t];if(r&&(i[r.entity_id]=r,"group"===(0,n.M)(r.entity_id))){const t=((e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const r=e[t];r&&(i[r.entity_id]=r)})),i})(e,r);Object.keys(t).forEach((e=>{const r=t[e];i[e]=r}))}})),i})(s,e),i={};return Object.keys(t).forEach(((e,t)=>{i[e]=t})),_(c,(0,o.p)(e.entity_id),(0,a.C)(e),e.attributes.icon,t,i)}));let u=e.location_name;return 0!==d.length&&"group.default_view"===d[0].entity_id||(h.unshift(E(t,i,r,s,c)),e.components.includes("geo_location")&&h[0]&&h[0].cards&&h[0].cards.push({type:"map",geo_location_sources:["all"]}),h.length>1&&"Home"===u&&(u="Home Assistant")),1===h.length&&0===h[0].cards.length&&h[0].cards.push({type:"empty-state"}),{title:u,views:h}},P=async(e,t)=>{if(e.config.state===r.UE)return{title:e.config.location_name,views:[{cards:[{type:"starting"}]}]};if(e.config.safe_mode)return{title:e.config.location_name,views:[{cards:[{type:"safe-mode"}]}]};b||(b=!0,(0,h.sG)(e.connection,(()=>{})),(0,u.q4)(e.connection,(()=>{})),(0,p.LM)(e.connection,(()=>{})));const[i,n,o]=await Promise.all([(0,d.l)(e.connection,h.sG),(0,d.l)(e.connection,u.q4),(0,d.l)(e.connection,p.LM)]);return C(e.config,i,n,o,e.states,t||e.localize)}},68500:(e,t,i)=>{"use strict";i.d(t,{k:()=>s});var r=i(69470);const n={},o={},s=(e,t)=>{e.forEach((e=>{const i=new URL(e.url,t).toString();switch(e.type){case"css":if(i in n)break;n[i]=(0,r.j)(i);break;case"js":if(i in o)break;o[i]=(0,r.fs)(i);break;case"module":(0,r.$y)(i);break;default:console.warn("Unknown resource type specified: "+e.type)}}));["/static/ais_dom/cards/card-tools.js?v=20201012","/static/ais_dom/cards/ais-tts.js","/static/ais_dom/cards/lovelace-swipe-navigation.js?v=20201101"].forEach((e=>{const i=new URL(e,t).toString();i in o||(o[i]=(0,r.fs)(i))}));["/static/ais_dom/cards/card-mod.js?v=20201012"].forEach((e=>{(0,r.$y)(new URL(e,t).toString())}))}},54324:(e,t,i)=>{"use strict";i.d(t,{Z0:()=>r,BN:()=>n,LG:()=>o,f1:()=>s,qD:()=>a,Y7:()=>l,wI:()=>c,Uo:()=>d,YI:()=>h,mA:()=>u,PT:()=>p});const r=(e,t,i)=>{const[r]=t,n=[];return e.views.forEach(((t,o)=>{if(o!==r)return void n.push(e.views[o]);const s=t.cards?[...t.cards,i]:[i];n.push({...t,cards:s})})),{...e,views:n}},n=(e,t,i)=>{const[r]=t,n=[];return e.views.forEach(((t,o)=>{if(o!==r)return void n.push(e.views[o]);const s=t.cards?[...t.cards,...i]:[...i];n.push({...t,cards:s})})),{...e,views:n}},o=(e,t,i)=>{const[r,n]=t,o=[];return e.views.forEach(((t,s)=>{s===r?o.push({...t,cards:(t.cards||[]).map(((e,t)=>t===n?i:e))}):o.push(e.views[s])})),{...e,views:o}},s=(e,t)=>{const[i,r]=t,n=[];return e.views.forEach(((t,o)=>{o===i?n.push({...t,cards:(t.cards||[]).filter(((e,t)=>t!==r))}):n.push(e.views[o])})),{...e,views:n}},a=(e,t,i)=>{const[r,n]=t,o=[];return e.views.forEach(((t,s)=>{if(s!==r)return void o.push(e.views[s]);const a=t.cards?[...t.cards.slice(0,n),i,...t.cards.slice(n)]:[i];o.push({...t,cards:a})})),{...e,views:o}},l=(e,t,i)=>{const r=e.views[t[0]].cards[t[1]],n=e.views[i[0]].cards[i[1]],o=e.views[t[0]],s={...o,cards:o.cards.map(((e,i)=>i===t[1]?n:e))},a=t[0]===i[0]?s:e.views[i[0]],l={...a,cards:a.cards.map(((e,t)=>t===i[1]?r:e))};return{...e,views:e.views.map(((e,r)=>r===i[0]?l:r===t[0]?s:e))}},c=(e,t,i)=>{if(t[0]===i[0])throw new Error("You can not move a card to the view it is in.");const r=e.views[t[0]],n=r.cards[t[1]],o={...r,cards:(r.cards||[]).filter(((e,i)=>i!==t[1]))},s=e.views[i[0]],a=s.cards?[...s.cards,n]:[n],l={...s,cards:a};return{...e,views:e.views.map(((e,r)=>r===i[0]?l:r===t[0]?o:e))}},d=(e,t)=>({...e,views:e.views.concat(t)}),h=(e,t,i)=>({...e,views:e.views.map(((e,r)=>r===t?i:e))}),u=(e,t,i)=>{const r=e.views[t],n=e.views[i];return{...e,views:e.views.map(((e,o)=>o===i?r:o===t?n:e))}},p=(e,t)=>({...e,views:e.views.filter(((e,i)=>i!==t))})},14748:(e,t,i)=>{"use strict";function r(e){return e.map((e=>"string"==typeof e?{entity:e}:e))}i.d(t,{Q:()=>r})},72922:(e,t,i)=>{"use strict";i.r(t);i(53918);var r=i(60461),n=i.n(r),o=i(15652),s=i(5986),a=i(15327),l=(i(48811),i(15291),i(81796)),c=i(17852),d=i(68500),h=i(47181);const u="show-save-config";let p=!1;i(81689);var f=i(55317);i(53268),i(85530);(0,i(28393).VA)("waterfall",{run:function(){this.shadow=this.isOnScreen()&&this.isContentBelow()}});i(12730),i(91441);var m=i(81471),v=i(14516),y=i(7323);var g=i(86977),w=i(83849),b=i(87744),k=i(38346),_=i(96151);i(81545),i(16509),i(25230),i(52039);function E(){E=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!$(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return O(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?O(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=A(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:S(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=S(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function C(e){var t,i=A(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function $(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function S(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function A(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function T(e,t,i){return(T="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=z(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function z(e){return(z=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var n=E();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(x(o.descriptor)||x(n.descriptor)){if($(o)||$(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if($(o)){if($(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}P(o,n)}else t.push(o)}return t}(s.d.map(C)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-icon-button-arrow-next")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.sz)()],key:"_icon",value:()=>f.aIO},{kind:"method",key:"connectedCallback",value:function(){T(z(i.prototype),"connectedCallback",this).call(this),setTimeout((()=>{this._icon="ltr"===window.getComputedStyle(this).direction?f.aIO:f.J3k}),100)}},{kind:"method",key:"render",value:function(){return o.dy`<mwc-icon-button .disabled=${this.disabled}>
      <ha-svg-icon .path=${this._icon}></ha-svg-icon>
    </mwc-icon-button> `}}]}}),o.oi);i(2315),i(48932),i(46167);var D=i(26765),j=i(51444),M=(i(27849),i(11654)),I=i(27322),R=i(54324);let F=!1;const L="show-edit-lovelace",V=(e,t)=>{F||(F=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:L,dialogTag:"hui-dialog-edit-lovelace",dialogImport:()=>Promise.all([i.e(5009),i.e(6964),i.e(5852)]).then(i.bind(i,74764))})})(e)),(0,h.B)(e,L,t)};let U=!1;const B="show-edit-view",N=(e,t)=>{U||(U=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:B,dialogTag:"hui-dialog-edit-view",dialogImport:()=>Promise.all([i.e(5009),i.e(4358),i.e(1041),i.e(8374),i.e(1458),i.e(8946),i.e(6087),i.e(5037),i.e(4535),i.e(6902),i.e(1153)]).then(i.bind(i,18632))})})(e)),(0,h.B)(e,B,t)};i(19961);function W(){W=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!Q(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Z(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?Z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=X(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=Y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function q(e){var t,i=X(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function H(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Q(e){return e.decorators&&e.decorators.length}function G(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function X(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Z(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function J(e,t,i){return(J="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=K(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function K(e){return(K=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let ee=function(e,t,i,r){var n=W();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(G(o.descriptor)||G(n.descriptor)){if(Q(o)||Q(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(Q(o)){if(Q(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}H(o,n)}else t.push(o)}return t}(s.d.map(q)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._debouncedConfigChanged=(0,k.D)((()=>this._selectView(this._curView,!0)),100,!1)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_curView",value:void 0},{kind:"field",decorators:[(0,o.IO)("ha-app-layout",!0)],key:"_appLayout",value:void 0},{kind:"field",key:"_viewCache",value:void 0},{kind:"field",key:"_debouncedConfigChanged",value:void 0},{kind:"field",key:"_conversation",value(){return(0,v.Z)((e=>(0,y.p)(this.hass,"conversation")))}},{kind:"method",key:"render",value:function(){var e,t,i;return o.dy`
      <ha-app-layout id="layout">
        <app-header
          slot="header"
          effects="waterfall"
          class=${(0,m.$)({"edit-mode":this._editMode})}
          fixed
          condenses
        >
          ${this._editMode?o.dy`
                <app-toolbar class="edit-mode">
                  <mwc-icon-button
                    .label="${this.hass.localize("ui.panel.lovelace.menu.exit_edit_mode")}"
                    title="${this.hass.localize("ui.panel.lovelace.menu.close")}"
                    @click="${this._editModeDisable}"
                  >
                    <ha-svg-icon .path=${f.r5M}></ha-svg-icon>
                  </mwc-icon-button>
                  <div main-title>
                    ${this.config.title||this.hass.localize("ui.panel.lovelace.editor.header")}
                    <mwc-icon-button
                      aria-label="${this.hass.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      title="${this.hass.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      class="edit-icon"
                      @click="${this._editLovelace}"
                    >
                      <ha-svg-icon .path=${f.r9}></ha-svg-icon>
                    </mwc-icon-button>
                  </div>
                  <a
                    href="${(0,I.R)(this.hass,"/lovelace/")}"
                    rel="noreferrer"
                    class="menu-link"
                    target="_blank"
                  >
                    <mwc-icon-button
                      title="${this.hass.localize("ui.panel.lovelace.menu.help")}"
                    >
                      <ha-svg-icon .path=${f.Xc_}></ha-svg-icon>
                    </mwc-icon-button>
                  </a>
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .title="${this.hass.localize("ui.panel.lovelace.editor.menu.open")}"
                      .label=${this.hass.localize("ui.panel.lovelace.editor.menu.open")}
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${o.dy`
                          <mwc-list-item
                            aria-label=${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            ${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                          </mwc-list-item>
                        `}
                    <mwc-list-item @request-selected="${this._handleRawEditor}">
                      ${this.hass.localize("ui.panel.lovelace.editor.menu.raw_editor")}
                    </mwc-list-item>
                  </ha-button-menu>
                </app-toolbar>
              `:o.dy`
                <app-toolbar>
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                  ${this.lovelace.config.views.length>1?o.dy`
                        <ha-tabs
                          scrollable
                          .selected="${this._curView}"
                          @iron-activate="${this._handleViewSelected}"
                          dir="${(0,b.Zu)(this.hass)}"
                        >
                          ${this.lovelace.config.views.map((e=>o.dy`
                              <paper-tab
                                aria-label="${e.title}"
                                class="${(0,m.$)({"hide-tab":Boolean(void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.hass.user.id))||!1===e.visible))})}"
                              >
                                ${e.icon?o.dy`
                                      <ha-icon
                                        title="${e.title}"
                                        .icon="${e.icon}"
                                      ></ha-icon>
                                    `:e.title||"Unnamed view"}
                              </paper-tab>
                            `))}
                        </ha-tabs>
                      `:o.dy`<div main-title>${this.config.title}</div>`}
                  ${!this.narrow&&this._conversation(this.hass.config.components)?o.dy`
                        <mwc-icon-button
                          .label=${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}
                          @click=${this._showVoiceCommandDialog}
                        >
                          <ha-svg-icon .path=${f.ewV}></ha-svg-icon>
                        </mwc-icon-button>
                      `:""}
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .label=${this.hass.localize("ui.panel.lovelace.editor.menu.open")}
                      .title="${this.hass.localize("ui.panel.lovelace.editor.menu.open")}"
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${this.narrow&&this._conversation(this.hass.config.components)?o.dy`
                          <mwc-list-item
                            .label=${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}
                            graphic="icon"
                            @request-selected=${this._showVoiceCommandDialog}
                          >
                            <span
                              >${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.N3O}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${this._yamlMode?o.dy`
                          <mwc-list-item
                            aria-label=${this.hass.localize("ui.panel.lovelace.menu.refresh")}
                            graphic="icon"
                            @request-selected="${this._handleRefresh}"
                          >
                            <span
                              >${this.hass.localize("ui.panel.lovelace.menu.refresh")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                          <mwc-list-item
                            aria-label=${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                            graphic="icon"
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            <span
                              >${this.hass.localize("ui.panel.lovelace.unused_entities.title")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.RIj}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${"yaml"===(null===(e=this.hass.panels.lovelace)||void 0===e||null===(t=e.config)||void 0===t?void 0:t.mode)?o.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.hass.localize("ui.panel.lovelace.menu.reload_resources")}
                            @request-selected=${this._handleReloadResources}
                          >
                            ${this.hass.localize("ui.panel.lovelace.menu.reload_resources")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${(null===(i=this.hass.user)||void 0===i?void 0:i.is_admin)&&!this.hass.config.safe_mode?o.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.hass.localize("ui.panel.lovelace.menu.configure_ui")}
                            @request-selected=${this._handleEnableEditMode}
                          >
                            ${this.hass.localize("ui.panel.lovelace.menu.configure_ui")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.Shd}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    <a
                      href="${(0,I.R)(this.hass,"/lovelace/")}"
                      rel="noreferrer"
                      class="menu-link"
                      target="_blank"
                    >
                      <mwc-list-item
                        graphic="icon"
                        aria-label=${this.hass.localize("ui.panel.lovelace.menu.help")}
                      >
                        ${this.hass.localize("ui.panel.lovelace.menu.help")}
                        <ha-svg-icon
                          slot="graphic"
                          .path=${f.HET}
                        ></ha-svg-icon>
                      </mwc-list-item>
                    </a>
                  </ha-button-menu>
                </app-toolbar>
              `}
          ${this._editMode?o.dy`
                <div sticky>
                  <ha-tabs
                    scrollable
                    .selected="${this._curView}"
                    @iron-activate="${this._handleViewSelected}"
                    dir="${(0,b.Zu)(this.hass)}"
                  >
                    ${this.lovelace.config.views.map((e=>o.dy`
                        <paper-tab
                          aria-label="${e.title}"
                          class="${(0,m.$)({"hide-tab":Boolean(!this._editMode&&void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.hass.user.id))||!1===e.visible))})}"
                        >
                          ${this._editMode?o.dy`
                                <ha-icon-button-arrow-prev
                                  title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_left")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewLeft}"
                                  ?disabled="${0===this._curView}"
                                ></ha-icon-button-arrow-prev>
                              `:""}
                          ${e.icon?o.dy`
                                <ha-icon
                                  title="${e.title}"
                                  .icon="${e.icon}"
                                ></ha-icon>
                              `:e.title||"Unnamed view"}
                          ${this._editMode?o.dy`
                                <ha-svg-icon
                                  title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.edit")}"
                                  class="edit-icon view"
                                  .path=${f.r9}
                                  @click="${this._editView}"
                                ></ha-svg-icon>
                                <ha-icon-button-arrow-next
                                  title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_right")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewRight}"
                                  ?disabled="${this._curView+1===this.lovelace.config.views.length}"
                                ></ha-icon-button-arrow-next>
                              `:""}
                        </paper-tab>
                      `))}
                    ${this._editMode?o.dy`
                          <mwc-icon-button
                            id="add-view"
                            @click="${this._addView}"
                            title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.add")}"
                          >
                            <ha-svg-icon .path=${f.qX5}></ha-svg-icon>
                          </mwc-icon-button>
                        `:""}
                  </ha-tabs>
                </div>
              `:""}
        </app-header>
        <div id="view" @ll-rebuild="${this._debouncedConfigChanged}"></div>
      </ha-app-layout>
    `}},{kind:"field",key:"_isVisible",value(){return e=>Boolean(this._editMode||void 0===e.visible||!0===e.visible||Array.isArray(e.visible)&&e.visible.some((e=>{var t;return e.user===(null===(t=this.hass.user)||void 0===t?void 0:t.id)})))}},{kind:"method",key:"updated",value:function(e){J(K(r.prototype),"updated",this).call(this,e);const t=this._viewRoot.lastChild;let i;e.has("hass")&&t&&(t.hass=this.hass),e.has("narrow")&&t&&(t.narrow=this.narrow);let n=!1;const o=this.route.path.split("/")[1];if(e.has("route")){const e=this.config.views;if(!o&&e.length)i=e.findIndex(this._isVisible),(0,w.c)(this,`${this.route.prefix}/${e[i].path||i}`,!0);else if("hass-unused-entities"===o)i="hass-unused-entities";else if(o){const t=o,r=Number(t);let n=0;for(let i=0;i<e.length;i++)if(e[i].path===t||i===r){n=i;break}i=n}}if(e.has("lovelace")){const r=e.get("lovelace");if(r&&r.config===this.lovelace.config||(n=!0),!r||r.editMode!==this.lovelace.editMode){const e=this.config&&this.config.views;(0,h.B)(this,"iron-resize"),"storage"===this.lovelace.mode&&"hass-unused-entities"===o&&(i=e.findIndex(this._isVisible),(0,w.c)(this,`${this.route.prefix}/${e[i].path||i}`,!0))}!n&&t&&(t.lovelace=this.lovelace)}(void 0!==i||n)&&(n&&void 0===i&&(i=this._curView),(0,_.T)((()=>this._selectView(i,n))))}},{kind:"get",key:"config",value:function(){return this.lovelace.config}},{kind:"get",key:"_yamlMode",value:function(){return"yaml"===this.lovelace.mode}},{kind:"get",key:"_editMode",value:function(){return this.lovelace.editMode}},{kind:"get",key:"_layout",value:function(){return this.shadowRoot.getElementById("layout")}},{kind:"get",key:"_viewRoot",value:function(){return this.shadowRoot.getElementById("view")}},{kind:"method",key:"_handleRefresh",value:function(e){(0,g.Q)(e)&&(0,h.B)(this,"config-refresh")}},{kind:"method",key:"_handleReloadResources",value:function(e){(0,g.Q)(e)&&(this.hass.callService("lovelace","reload_resources"),(0,D.g7)(this,{title:this.hass.localize("ui.panel.lovelace.reload_resources.refresh_header"),text:this.hass.localize("ui.panel.lovelace.reload_resources.refresh_body"),confirm:()=>location.reload()}))}},{kind:"method",key:"_handleRawEditor",value:function(e){(0,g.Q)(e)&&this.lovelace.enableFullEditMode()}},{kind:"method",key:"_handleUnusedEntities",value:function(e){var t;(0,g.Q)(e)&&(0,w.c)(this,(null===(t=this.route)||void 0===t?void 0:t.prefix)+"/hass-unused-entities")}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,j._)(this)}},{kind:"method",key:"_handleEnableEditMode",value:function(e){(0,g.Q)(e)&&(this._yamlMode?(0,D.Ys)(this,{text:"The edit UI is not available when in YAML mode."}):this._enableEditMode())}},{kind:"method",key:"_enableEditMode",value:function(){this.lovelace.setEditMode(!0)}},{kind:"method",key:"_editModeDisable",value:function(){this.lovelace.setEditMode(!1)}},{kind:"method",key:"_editLovelace",value:function(){V(this,this.lovelace)}},{kind:"method",key:"_editView",value:function(){N(this,{lovelace:this.lovelace,viewIndex:this._curView})}},{kind:"method",key:"_moveViewLeft",value:function(){if(0===this._curView)return;const e=this.lovelace,t=this._curView,i=this._curView-1;this._curView=i,e.saveConfig((0,R.mA)(e.config,t,i))}},{kind:"method",key:"_moveViewRight",value:function(){if(this._curView+1===this.lovelace.config.views.length)return;const e=this.lovelace,t=this._curView,i=this._curView+1;this._curView=i,e.saveConfig((0,R.mA)(e.config,t,i))}},{kind:"method",key:"_addView",value:function(){N(this,{lovelace:this.lovelace,saveCallback:(e,t)=>{var i;const r=t.path||e;(0,w.c)(this,`${null===(i=this.route)||void 0===i?void 0:i.prefix}/${r}`)}})}},{kind:"method",key:"_handleViewSelected",value:function(e){const t=e.detail.selected;if(t!==this._curView){var i;const e=this.config.views[t].path||t;(0,w.c)(this,`${null===(i=this.route)||void 0===i?void 0:i.prefix}/${e}`)}!function(e,t){const i=t,r=Math.random(),n=Date.now(),o=i.scrollTop,s=0-o;e._currentAnimationId=r,function t(){const a=Date.now()-n;var l;a>200?i.scrollTop=0:e._currentAnimationId===r&&(i.scrollTop=(l=a,-s*(l/=200)*(l-2)+o),requestAnimationFrame(t.bind(e)))}.call(e)}(this,this._layout.header.scrollTarget)}},{kind:"method",key:"_selectView",value:function(e,t){if(!t&&this._curView===e)return;e=void 0===e?0:e,this._curView=e,t&&(this._viewCache={});const r=this._viewRoot;if(r.lastChild&&r.removeChild(r.lastChild),"hass-unused-entities"===e){const e=document.createElement("hui-unused-entities");return Promise.all([i.e(9160),i.e(3330),i.e(9395),i.e(9779),i.e(1929)]).then(i.bind(i,28279)).then((()=>{e.hass=this.hass,e.lovelace=this.lovelace,e.narrow=this.narrow})),void r.appendChild(e)}let n;const o=this.config.views[e];if(!o)return void this._enableEditMode();!t&&this._viewCache[e]?n=this._viewCache[e]:(n=document.createElement("hui-view"),n.index=e,this._viewCache[e]=n),n.lovelace=this.lovelace,n.hass=this.hass,n.narrow=this.narrow;const s=o.background||this.config.background;s?this._appLayout.style.setProperty("--lovelace-background",s):this._appLayout.style.removeProperty("--lovelace-background"),r.appendChild(n),(0,h.B)(this,"iron-resize")}},{kind:"get",static:!0,key:"styles",value:function(){return[M.Qx,o.iv`
        :host {
          --dark-color: #455a64;
          --text-dark-color: #fff;
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
        }

        ha-app-layout {
          min-height: 100%;
          background: var(
            --lovelace-background,
            var(--primary-background-color)
          );
        }
        ha-tabs {
          width: 100%;
          height: 100%;
          margin-left: 4px;
          --paper-tabs-selection-bar-color: var(--text-primary-color, #fff);
          text-transform: uppercase;
        }
        .edit-mode ha-tabs {
          margin-left: max(env(safe-area-inset-left), 24px);
          margin-right: max(env(safe-area-inset-right), 24px);
        }
        .edit-mode {
          background-color: var(--dark-color, #455a64);
          color: var(--text-dark-color);
        }
        .edit-mode div[main-title] {
          pointer-events: auto;
        }
        paper-tab.iron-selected .edit-icon {
          display: inline-flex;
        }
        .edit-icon {
          color: var(--accent-color);
          padding-left: 8px;
          vertical-align: middle;
          --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
        }
        .edit-icon.view {
          display: none;
        }
        #add-view {
          position: absolute;
          height: 44px;
        }
        #add-view ha-svg-icon {
          background-color: var(--accent-color);
          border-radius: 4px;
        }
        app-toolbar a {
          color: var(--text-primary-color, white);
        }
        mwc-button.warning:not([disabled]) {
          color: var(--error-color);
        }
        #view {
          min-height: calc(100vh - var(--header-height));
          /**
          * Since we only set min-height, if child nodes need percentage
          * heights they must use absolute positioning so we need relative
          * positioning here.
          *
          * https://www.w3.org/TR/CSS2/visudet.html#the-height-property
          */
          position: relative;
          display: flex;
        }
        #view > * {
          /**
          * The view could get larger than the window in Firefox
          * to prevent that we set the max-width to 100%
          * flex-grow: 1 and flex-basis: 100% should make sure the view
          * stays full width.
          *
          * https://github.com/home-assistant/home-assistant-polymer/pull/3806
          */
          flex: 1 1 100%;
          max-width: 100%;
        }
        .hide-tab {
          display: none;
        }
        .menu-link {
          text-decoration: none;
        }
      `]}}]}}),o.oi);function te(){te=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ne(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return le(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?le(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=ae(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:se(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=se(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function ie(e){var t,i=ae(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function re(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ne(e){return e.decorators&&e.decorators.length}function oe(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function se(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function ae(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function le(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function ce(e,t,i){return(ce="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=de(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function de(e){return(de=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}customElements.define("hui-root",ee),window.loadCardHelpers=()=>Promise.all([i.e(4909),i.e(319),i.e(7282),i.e(2016),i.e(5457)]).then(i.bind(i,49686));let he=!1,ue=!1,pe=function(e,t,i,r){var n=te();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(oe(o.descriptor)||oe(n.descriptor)){if(ne(o)||ne(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ne(o)){if(ne(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}re(o,n)}else t.push(o)}return t}(s.d.map(ie)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._closeEditor=this._closeEditor.bind(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)()],key:"panel",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"_state",value:()=>"loading"},{kind:"field",decorators:[(0,o.sz)()],key:"_errorMsg",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"lovelace",value:void 0},{kind:"field",key:"_ignoreNextUpdateEvent",value:()=>!1},{kind:"field",key:"_fetchConfigOnConnect",value:()=>!1},{kind:"field",key:"_unsubUpdates",value:void 0},{kind:"method",key:"connectedCallback",value:function(){ce(de(r.prototype),"connectedCallback",this).call(this),this.lovelace&&this.hass&&this.lovelace.language!==this.hass.language?this._setLovelaceConfig(this.lovelace.config,this.lovelace.mode):this.lovelace&&"generated"===this.lovelace.mode?(this._state="loading",this._regenerateConfig()):this._fetchConfigOnConnect&&this._fetchConfig(!1)}},{kind:"method",key:"disconnectedCallback",value:function(){ce(de(r.prototype),"disconnectedCallback",this).call(this),null!==this.urlPath&&this._unsubUpdates&&this._unsubUpdates()}},{kind:"method",key:"render",value:function(){const e=this._state;return"loaded"===e?o.dy`
        <hui-root
          .hass=${this.hass}
          .lovelace=${this.lovelace}
          .route=${this.route}
          .narrow=${this.narrow}
          @config-refresh=${this._forceFetchConfig}
        ></hui-root>
      `:"error"===e?o.dy`
        <hass-error-screen
          title="${(0,s.Lh)(this.hass.localize,"lovelace")}"
          .error="${this._errorMsg}"
        >
          <mwc-button raised @click=${this._forceFetchConfig}>
            ${this.hass.localize("ui.panel.lovelace.reload_lovelace")}
          </mwc-button>
        </hass-error-screen>
      `:"yaml-editor"===e?o.dy`
        <hui-editor
          .hass=${this.hass}
          .lovelace="${this.lovelace}"
          .closeEditor="${this._closeEditor}"
        ></hui-editor>
      `:o.dy`
      <hass-loading-screen
        rootnav
        .hass=${this.hass}
        .narrow=${this.narrow}
      ></hass-loading-screen>
    `}},{kind:"method",key:"firstUpdated",value:function(){this._fetchConfig(!1),this._unsubUpdates||this._subscribeUpdates(),window.addEventListener("connection-status",(e=>{"connected"===e.detail&&this._fetchConfig(!1)}))}},{kind:"method",key:"_regenerateConfig",value:async function(){const e=await(0,c.UO)(this.hass);this._setLovelaceConfig(e,"generated"),this._state="loaded"}},{kind:"method",key:"_subscribeUpdates",value:async function(){this._unsubUpdates=await(0,a.Gc)(this.hass.connection,this.urlPath,(()=>this._lovelaceChanged()))}},{kind:"method",key:"_closeEditor",value:function(){this._state="loaded"}},{kind:"method",key:"_lovelaceChanged",value:function(){this._ignoreNextUpdateEvent?this._ignoreNextUpdateEvent=!1:this.isConnected?(0,l.C)(this,{message:this.hass.localize("ui.panel.lovelace.changed_toast.message"),action:{action:()=>this._fetchConfig(!1),text:this.hass.localize("ui.panel.lovelace.changed_toast.refresh")},duration:0,dismissable:!1}):this._fetchConfigOnConnect=!0}},{kind:"get",key:"urlPath",value:function(){return"lovelace"===this.panel.url_path?null:this.panel.url_path}},{kind:"method",key:"_forceFetchConfig",value:function(){this._fetchConfig(!0)}},{kind:"method",key:"_fetchConfig",value:async function(e){let t,i,r=this.panel.config.mode;const n=window;n.llConfProm&&(i=n.llConfProm,n.llConfProm=void 0),ue||(ue=!0,(n.llConfProm||(0,a.eL)(this.hass.connection)).then((e=>(0,d.k)(e,this.hass.auth.data.hassUrl)))),null===this.urlPath&&i||(this.lovelace&&"yaml"===this.lovelace.mode&&(this._ignoreNextUpdateEvent=!0),i=(0,a.Q2)(this.hass.connection,this.urlPath,e));try{t=await i}catch(o){if("config_not_found"!==o.code)return console.log(o),this._state="error",void(this._errorMsg=o.message);const e=await this.hass.loadBackendTranslation("title");t=await(0,c.UO)(this.hass,e),r="generated"}finally{this.lovelace&&"yaml"===this.lovelace.mode&&setTimeout((()=>{this._ignoreNextUpdateEvent=!1}),2e3)}this._state="loaded",this._setLovelaceConfig(t,r)}},{kind:"method",key:"_checkLovelaceConfig",value:function(e){let t=Object.isFrozen(e)?void 0:e;return e.views.forEach(((i,r)=>{i.badges&&!i.badges.every(Boolean)&&(t=t||{...e,views:[...e.views]},t.views[r]={...i},t.views[r].badges=i.badges.filter(Boolean))})),t?n()(t):e}},{kind:"method",key:"_setLovelaceConfig",value:function(e,t){e=this._checkLovelaceConfig(e);const r=this.urlPath;this.lovelace={config:e,mode:t,urlPath:this.urlPath,editMode:!!this.lovelace&&this.lovelace.editMode,language:this.hass.language,enableFullEditMode:()=>{he||(he=!0,Promise.all([i.e(9033),i.e(1572),i.e(3822),i.e(2747)]).then(i.bind(i,95912))),this._state="yaml-editor"},setEditMode:e=>{var t,r;e&&"generated"===this.lovelace.mode?(t=this,r={lovelace:this.lovelace,mode:this.panel.config.mode},p||(p=!0,(0,h.B)(t,"register-dialog",{dialogShowEvent:u,dialogTag:"hui-dialog-save-config",dialogImport:()=>Promise.all([i.e(1458),i.e(9033),i.e(1572),i.e(3822),i.e(4538)]).then(i.bind(i,78082))})),(0,h.B)(t,u,r)):this._updateLovelace({editMode:e})},saveConfig:async e=>{const{config:t,mode:i}=this.lovelace;e=this._checkLovelaceConfig(e);try{this._updateLovelace({config:e,mode:"storage"}),this._ignoreNextUpdateEvent=!0,await(0,a.Oh)(this.hass,r,e)}catch(n){throw console.error(n),this._updateLovelace({config:t,mode:i}),n}},deleteConfig:async()=>{const{config:e,mode:t}=this.lovelace;try{const e=await this.hass.loadBackendTranslation("title");this._updateLovelace({config:await(0,c.UO)(this.hass,e),mode:"generated",editMode:!1}),this._ignoreNextUpdateEvent=!0,await(0,a.vj)(this.hass,r)}catch(i){throw console.error(i),this._updateLovelace({config:e,mode:t}),i}}}}},{kind:"method",key:"_updateLovelace",value:function(e){this.lovelace={...this.lovelace,...e}}}]}}),o.oi);customElements.define("ha-panel-lovelace",pe)},27322:(e,t,i)=>{"use strict";i.d(t,{R:()=>r});const r=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=chunk.9bc3dc3319763c6b9bbe.js.map