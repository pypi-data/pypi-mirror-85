(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6327],{47181:function(t,e,n){"use strict";n.d(e,{B:function(){return o}});var o=function(t,e,n,o){o=o||{},n=null==n?{}:n;var r=new Event(e,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return r.detail=n,t.dispatchEvent(r),r}},86327:function(t,e,n){"use strict";n.r(e);var o=n(47181);function r(t){return(r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function i(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function c(t,e){for(var n=0;n<e.length;n++){var o=e[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}function u(t,e){return!e||"object"!==r(e)&&"function"!=typeof e?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function s(t){var e="function"==typeof Map?new Map:void 0;return(s=function(t){if(null===t||(n=t,-1===Function.toString.call(n).indexOf("[native code]")))return t;var n;if("function"!=typeof t)throw new TypeError("Super expression must either be null or a function");if(void 0!==e){if(e.has(t))return e.get(t);e.set(t,o)}function o(){return a(t,arguments,p(this).constructor)}return o.prototype=Object.create(t.prototype,{constructor:{value:o,enumerable:!1,writable:!0,configurable:!0}}),l(o,t)})(t)}function a(t,e,n){return(a=f()?Reflect.construct:function(t,e,n){var o=[null];o.push.apply(o,e);var r=new(Function.bind.apply(t,o));return n&&l(r,n.prototype),r}).apply(null,arguments)}function f(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function l(t,e){return(l=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function p(t){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var y=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&l(t,e)}(h,t);var e,n,r,s,a,y=(e=h,n=f(),function(){var t,o=p(e);if(n){var r=p(this).constructor;t=Reflect.construct(o,arguments,r)}else t=o.apply(this,arguments);return u(this,t)});function h(){return i(this,h),y.apply(this,arguments)}return r=h,(s=[{key:"_onClick",value:function(){(0,o.B)(this,"hass-more-info",{entityId:this.config.entity})}},{key:"setConfig",value:function(t){if(!t.entity)throw new Error("You need to define an entity");this.config=t}},{key:"getCardSize",value:function(){return 3}},{key:"hass",set:function(t){if(!this.content){var e=document.createElement("ha-card");this.content=document.createElement("div"),e.appendChild(this.content),e.style="background: none;",this.appendChild(e),this.addEventListener("click",(function(){this._onClick()}))}var n=this.config.off_image,o=this.config.entity,r=t.states[o],i=r?r.state:"unavailable",c=this.config.class||this.config.entity.replace(".","_");if(this.setAttribute("class",c),r){var u=r.attributes.entity_picture;this.content.innerHTML="playing"===i&&u?'<img src="'.concat(u,'" width=100% height=100%" style="">'):n?'<img src="'.concat(n,'" width=100% align="center" style="">'):'<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}else this.content.innerHTML='<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}}])&&c(r.prototype,s),a&&c(r,a),h}(s(HTMLElement));customElements.define("hui-ais-now-playing-poster-card",y)}}]);
//# sourceMappingURL=chunk.0ea66788d12713c270c5.js.map