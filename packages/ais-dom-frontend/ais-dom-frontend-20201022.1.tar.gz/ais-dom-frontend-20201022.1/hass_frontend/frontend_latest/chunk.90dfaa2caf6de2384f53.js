/*! For license information please see chunk.90dfaa2caf6de2384f53.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1384,2926,5037],{8470:(e,t,i)=>{"use strict";i.d(t,{o:()=>n});const n=i(15652).iv`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch)[dir=rtl]{margin-left:10px}`},50190:(e,t,i)=>{"use strict";var n=i(87480),o=i(15652),r=i(72774),a={ROOT:"mdc-form-field"},l={LABEL_SELECTOR:".mdc-form-field > label"};const s=function(e){function t(i){var o=e.call(this,(0,n.pi)((0,n.pi)({},t.defaultAdapter),i))||this;return o.click=function(){o.handleClick()},o}return(0,n.ZT)(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return a},enumerable:!0,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return l},enumerable:!0,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!0,configurable:!0}),t.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},t.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},t.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},t}(r.K);var d=i(78220),p=i(18601),c=i(14114),h=i(82612),m=i(81471);class f extends d.H{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=s}createAdapter(){return{registerInteractionHandler:(e,t)=>{this.labelEl.addEventListener(e,t)},deregisterInteractionHandler:(e,t)=>{this.labelEl.removeEventListener(e,t)},activateInputRipple:async()=>{const e=this.input;if(e instanceof p.Wg){const t=await e.ripple;t&&t.startPress()}},deactivateInputRipple:async()=>{const e=this.input;if(e instanceof p.Wg){const t=await e.ripple;t&&t.endPress()}}}}get input(){return(0,h.f6)(this.slotEl,"*")}render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return o.dy`
      <div class="mdc-form-field ${(0,m.$)(e)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const e=this.input;e&&(e.focus(),e.click())}}(0,n.gn)([(0,o.Cb)({type:Boolean})],f.prototype,"alignEnd",void 0),(0,n.gn)([(0,o.Cb)({type:Boolean})],f.prototype,"spaceBetween",void 0),(0,n.gn)([(0,o.Cb)({type:Boolean})],f.prototype,"nowrap",void 0),(0,n.gn)([(0,o.Cb)({type:String}),(0,c.P)((async function(e){const t=this.input;t&&("input"===t.localName?t.setAttribute("aria-label",e):t instanceof p.Wg&&(await t.updateComplete,t.setAriaLabel(e)))}))],f.prototype,"label",void 0),(0,n.gn)([(0,o.IO)(".mdc-form-field")],f.prototype,"mdcRoot",void 0),(0,n.gn)([(0,o.IO)("slot")],f.prototype,"slotEl",void 0),(0,n.gn)([(0,o.IO)("label")],f.prototype,"labelEl",void 0);var u=i(8470);let g=class extends f{};g.styles=u.o,g=(0,n.gn)([(0,o.Mo)("mwc-formfield")],g)},68646:(e,t,i)=>{"use strict";i.d(t,{B:()=>a});var n=i(87480),o=(i(66702),i(98734)),r=i(15652);class a extends r.oi{constructor(){super(...arguments),this.disabled=!1,this.icon="",this.label="",this.shouldRenderRipple=!1,this.rippleHandlers=new o.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}renderRipple(){return this.shouldRenderRipple?r.dy`
            <mwc-ripple
                .disabled="${this.disabled}"
                unbounded>
            </mwc-ripple>`:""}focus(){const e=this.buttonElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.buttonElement;e&&(this.rippleHandlers.endFocus(),e.blur())}render(){return r.dy`<button
        class="mdc-icon-button"
        aria-label="${this.label||this.icon}"
        ?disabled="${this.disabled}"
        @focus="${this.handleRippleFocus}"
        @blur="${this.handleRippleBlur}"
        @mousedown="${this.handleRippleMouseDown}"
        @mouseenter="${this.handleRippleMouseEnter}"
        @mouseleave="${this.handleRippleMouseLeave}"
        @touchstart="${this.handleRippleTouchStart}"
        @touchend="${this.handleRippleDeactivate}"
        @touchcancel="${this.handleRippleDeactivate}">
      ${this.renderRipple()}
    <i class="material-icons">${this.icon}</i>
    <span class="default-slot-container">
        <slot></slot>
    </span>
  </button>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,n.gn)([(0,r.Cb)({type:Boolean,reflect:!0})],a.prototype,"disabled",void 0),(0,n.gn)([(0,r.Cb)({type:String})],a.prototype,"icon",void 0),(0,n.gn)([(0,r.Cb)({type:String})],a.prototype,"label",void 0),(0,n.gn)([(0,r.IO)("button")],a.prototype,"buttonElement",void 0),(0,n.gn)([(0,r.GC)("mwc-ripple")],a.prototype,"ripple",void 0),(0,n.gn)([(0,r.sz)()],a.prototype,"shouldRenderRipple",void 0),(0,n.gn)([(0,r.hO)({passive:!0})],a.prototype,"handleRippleMouseDown",null),(0,n.gn)([(0,r.hO)({passive:!0})],a.prototype,"handleRippleTouchStart",null)},81383:(e,t,i)=>{"use strict";i.d(t,{o:()=>n});const n=i(15652).iv`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:none;background-color:transparent;fill:currentColor;color:inherit;font-size:24px;text-decoration:none;cursor:pointer;user-select:none;width:48px;height:48px;padding:12px}.mdc-icon-button svg,.mdc-icon-button img{width:24px;height:24px}.mdc-icon-button:disabled{color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-disabled-on-light, rgba(0, 0, 0, 0.38))}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}:host{display:inline-block;outline:none;--mdc-ripple-color: currentcolor}:host([disabled]){pointer-events:none}:host,.mdc-icon-button{vertical-align:top}.mdc-icon-button{width:var(--mdc-icon-button-size, 48px);height:var(--mdc-icon-button-size, 48px);padding:calc((var(--mdc-icon-button-size, 48px) - var(--mdc-icon-size, 24px)) / 2)}.mdc-icon-button>i{position:absolute;top:0;padding-top:inherit}.mdc-icon-button i,.mdc-icon-button svg,.mdc-icon-button img,.mdc-icon-button ::slotted(*){display:block;width:var(--mdc-icon-size, 24px);height:var(--mdc-icon-size, 24px)}`},25230:(e,t,i)=>{"use strict";var n=i(87480),o=i(15652),r=i(68646),a=i(81383);let l=class extends r.B{};l.styles=a.o,l=(0,n.gn)([(0,o.Mo)("mwc-icon-button")],l)},25782:(e,t,i)=>{"use strict";i(43437),i(65660),i(70019),i(97968);var n=i(9672),o=i(50856),r=i(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[r.U]})},89194:(e,t,i)=>{"use strict";i(43437),i(65660),i(70019);var n=i(9672),o=i(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},1275:(e,t,i)=>{"use strict";i.d(t,{l:()=>r});var n=i(94707);const o=new WeakMap,r=(0,n.XM)(((e,t)=>i=>{const n=o.get(i);if(Array.isArray(e)){if(Array.isArray(n)&&n.length===e.length&&e.every(((e,t)=>e===n[t])))return}else if(n===e&&(void 0!==e||o.has(i)))return;i.setValue(t()),o.set(i,Array.isArray(e)?Array.from(e):e)}))},14516:(e,t,i)=>{"use strict";i.d(t,{Z:()=>o});var n=function(e,t){return e.length===t.length&&e.every((function(e,i){return n=e,o=t[i],n===o;var n,o}))};const o=function(e,t){var i;void 0===t&&(t=n);var o,r=[],a=!1;return function(){for(var n=arguments.length,l=new Array(n),s=0;s<n;s++)l[s]=arguments[s];return a&&i===this&&t(l,r)||(o=e.apply(this,l),a=!0,i=this,r=l),o}}}}]);
//# sourceMappingURL=chunk.90dfaa2caf6de2384f53.js.map