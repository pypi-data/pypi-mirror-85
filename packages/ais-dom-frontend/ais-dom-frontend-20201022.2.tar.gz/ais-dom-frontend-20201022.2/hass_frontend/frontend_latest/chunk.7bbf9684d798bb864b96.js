/*! For license information please see chunk.7bbf9684d798bb864b96.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4582,7364,9462,1199,6964,3047],{27815:(t,e)=>{"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.shouldPolyfill=void 0,e.shouldPolyfill=function(){return"undefined"==typeof Intl||!("PluralRules"in Intl)||"one"===new Intl.PluralRules("en",{minimumFractionDigits:2}).select(1)}},3071:(t,e,n)=>{"use strict";n.d(e,{X:()=>s});var i=n(87480),r=(n(70475),n(66702),n(98734)),o=n(15652),a=n(81471);class s extends o.oi{constructor(){super(...arguments),this.raised=!1,this.unelevated=!1,this.outlined=!1,this.dense=!1,this.disabled=!1,this.trailingIcon=!1,this.fullwidth=!1,this.icon="",this.label="",this.expandContent=!1,this.shouldRenderRipple=!1,this.rippleHandlers=new r.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}renderRipple(){const t=this.raised||this.unelevated;return this.shouldRenderRipple?o.dy`<mwc-ripple .primary="${!t}" .disabled="${this.disabled}"></mwc-ripple>`:""}createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}focus(){const t=this.buttonElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.buttonElement;t&&(this.rippleHandlers.endFocus(),t.blur())}getRenderClasses(){return(0,a.$)({"mdc-button--raised":this.raised,"mdc-button--unelevated":this.unelevated,"mdc-button--outlined":this.outlined,"mdc-button--dense":this.dense})}render(){return o.dy`
      <button
          id="button"
          class="mdc-button ${this.getRenderClasses()}"
          ?disabled="${this.disabled}"
          aria-label="${this.label||this.icon}"
          @focus="${this.handleRippleFocus}"
          @blur="${this.handleRippleBlur}"
          @mousedown="${this.handleRippleActivate}"
          @mouseenter="${this.handleRippleMouseEnter}"
          @mouseleave="${this.handleRippleMouseLeave}"
          @touchstart="${this.handleRippleActivate}"
          @touchend="${this.handleRippleDeactivate}"
          @touchcancel="${this.handleRippleDeactivate}">
        ${this.renderRipple()}
        <span class="leading-icon">
          <slot name="icon">
            ${this.icon&&!this.trailingIcon?this.renderIcon():""}
          </slot>
        </span>
        <span class="mdc-button__label">${this.label}</span>
        <span class="slot-container ${(0,a.$)({flex:this.expandContent})}">
          <slot></slot>
        </span>
        <span class="trailing-icon">
          <slot name="trailingIcon">
            ${this.icon&&this.trailingIcon?this.renderIcon():""}
          </slot>
        </span>
      </button>`}renderIcon(){return o.dy`
    <mwc-icon class="mdc-button__icon">
      ${this.icon}
    </mwc-icon>`}handleRippleActivate(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,i.gn)([(0,o.Cb)({type:Boolean})],s.prototype,"raised",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean})],s.prototype,"unelevated",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean})],s.prototype,"outlined",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean})],s.prototype,"dense",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean,attribute:"trailingicon"})],s.prototype,"trailingIcon",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean,reflect:!0})],s.prototype,"fullwidth",void 0),(0,i.gn)([(0,o.Cb)({type:String})],s.prototype,"icon",void 0),(0,i.gn)([(0,o.Cb)({type:String})],s.prototype,"label",void 0),(0,i.gn)([(0,o.Cb)({type:Boolean})],s.prototype,"expandContent",void 0),(0,i.gn)([(0,o.IO)("#button")],s.prototype,"buttonElement",void 0),(0,i.gn)([(0,o.GC)("mwc-ripple")],s.prototype,"ripple",void 0),(0,i.gn)([(0,o.sz)()],s.prototype,"shouldRenderRipple",void 0),(0,i.gn)([(0,o.hO)({passive:!0})],s.prototype,"handleRippleActivate",null)},53918:(t,e,n)=>{"use strict";var i=n(87480),r=n(15652),o=n(3071),a=n(97591);let s=class extends o.X{};s.styles=a.o,s=(0,i.gn)([(0,r.Mo)("mwc-button")],s)},97591:(t,e,n)=>{"use strict";n.d(e,{o:()=>i});const i=n(15652).iv`.mdc-touch-target-wrapper{display:inline}.mdc-elevation-overlay{position:absolute;border-radius:inherit;pointer-events:none;opacity:0;opacity:var(--mdc-elevation-overlay-opacity, 0);transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff;background-color:var(--mdc-elevation-overlay-color, #fff)}.mdc-button{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);padding:0 8px 0 8px;position:relative;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;min-width:64px;border:none;outline:none;line-height:inherit;user-select:none;-webkit-appearance:none;overflow:visible;vertical-align:middle;border-radius:4px;border-radius:var(--mdc-shape-small, 4px);height:36px}.mdc-button .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}.mdc-button::-moz-focus-inner{padding:0;border:0}.mdc-button:active{outline:none}.mdc-button:hover{cursor:pointer}.mdc-button:disabled{cursor:default;pointer-events:none}.mdc-button .mdc-button__ripple{border-radius:4px;border-radius:var(--mdc-shape-small, 4px)}.mdc-button:not(:disabled){background-color:transparent}.mdc-button:disabled{background-color:transparent}.mdc-button .mdc-button__icon{margin-left:0;margin-right:8px;display:inline-block;width:18px;height:18px;font-size:18px;vertical-align:top}[dir=rtl] .mdc-button .mdc-button__icon,.mdc-button .mdc-button__icon[dir=rtl]{margin-left:8px;margin-right:0}.mdc-button .mdc-button__touch{position:absolute;top:50%;right:0;height:48px;left:0;transform:translateY(-50%)}.mdc-button:not(:disabled){color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}.mdc-button:disabled{color:rgba(0, 0, 0, 0.38)}.mdc-button__label+.mdc-button__icon{margin-left:8px;margin-right:0}[dir=rtl] .mdc-button__label+.mdc-button__icon,.mdc-button__label+.mdc-button__icon[dir=rtl]{margin-left:0;margin-right:8px}svg.mdc-button__icon{fill:currentColor}.mdc-button--raised .mdc-button__icon,.mdc-button--unelevated .mdc-button__icon,.mdc-button--outlined .mdc-button__icon{margin-left:-4px;margin-right:8px}[dir=rtl] .mdc-button--raised .mdc-button__icon,.mdc-button--raised .mdc-button__icon[dir=rtl],[dir=rtl] .mdc-button--unelevated .mdc-button__icon,.mdc-button--unelevated .mdc-button__icon[dir=rtl],[dir=rtl] .mdc-button--outlined .mdc-button__icon,.mdc-button--outlined .mdc-button__icon[dir=rtl]{margin-left:8px;margin-right:-4px}.mdc-button--raised .mdc-button__label+.mdc-button__icon,.mdc-button--unelevated .mdc-button__label+.mdc-button__icon,.mdc-button--outlined .mdc-button__label+.mdc-button__icon{margin-left:8px;margin-right:-4px}[dir=rtl] .mdc-button--raised .mdc-button__label+.mdc-button__icon,.mdc-button--raised .mdc-button__label+.mdc-button__icon[dir=rtl],[dir=rtl] .mdc-button--unelevated .mdc-button__label+.mdc-button__icon,.mdc-button--unelevated .mdc-button__label+.mdc-button__icon[dir=rtl],[dir=rtl] .mdc-button--outlined .mdc-button__label+.mdc-button__icon,.mdc-button--outlined .mdc-button__label+.mdc-button__icon[dir=rtl]{margin-left:-4px;margin-right:8px}.mdc-button--raised,.mdc-button--unelevated{padding:0 16px 0 16px}.mdc-button--raised:not(:disabled),.mdc-button--unelevated:not(:disabled){background-color:#6200ee;background-color:var(--mdc-theme-primary, #6200ee)}.mdc-button--raised:not(:disabled),.mdc-button--unelevated:not(:disabled){color:#fff;color:var(--mdc-theme-on-primary, #fff)}.mdc-button--raised:disabled,.mdc-button--unelevated:disabled{background-color:rgba(0, 0, 0, 0.12)}.mdc-button--raised:disabled,.mdc-button--unelevated:disabled{color:rgba(0, 0, 0, 0.38)}.mdc-button--raised{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-button--raised:hover,.mdc-button--raised:focus{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12)}.mdc-button--raised:active{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}.mdc-button--raised:disabled{box-shadow:0px 0px 0px 0px rgba(0, 0, 0, 0.2),0px 0px 0px 0px rgba(0, 0, 0, 0.14),0px 0px 0px 0px rgba(0,0,0,.12)}.mdc-button--outlined{padding:0 15px 0 15px;border-width:1px;border-style:solid}.mdc-button--outlined .mdc-button__ripple{top:-1px;left:-1px;border:1px solid transparent}.mdc-button--outlined .mdc-button__touch{left:-1px;width:calc(100% + 2 * 1px)}.mdc-button--outlined:not(:disabled){border-color:rgba(0, 0, 0, 0.12)}.mdc-button--outlined:disabled{border-color:rgba(0, 0, 0, 0.12)}.mdc-button--touch{margin-top:6px;margin-bottom:6px}:host{display:inline-flex;outline:none;vertical-align:top}:host([fullwidth]){width:100%}:host([raised]),:host([unelevated]){--mdc-ripple-color: #fff;--mdc-ripple-focus-opacity: 0.24;--mdc-ripple-hover-opacity: 0.08;--mdc-ripple-press-opacity: 0.24}.trailing-icon ::slotted(*),.trailing-icon .mdc-button__icon,.leading-icon ::slotted(*),.leading-icon .mdc-button__icon{margin-left:0;margin-right:8px;display:inline-block;width:18px;height:18px;font-size:18px;vertical-align:top}[dir=rtl] .trailing-icon ::slotted(*),.trailing-icon ::slotted(*)[dir=rtl],[dir=rtl] .trailing-icon .mdc-button__icon,.trailing-icon .mdc-button__icon[dir=rtl],[dir=rtl] .leading-icon ::slotted(*),.leading-icon ::slotted(*)[dir=rtl],[dir=rtl] .leading-icon .mdc-button__icon,.leading-icon .mdc-button__icon[dir=rtl]{margin-left:8px;margin-right:0}.trailing-icon ::slotted(*),.trailing-icon .mdc-button__icon{margin-left:8px;margin-right:0}[dir=rtl] .trailing-icon ::slotted(*),.trailing-icon ::slotted(*)[dir=rtl],[dir=rtl] .trailing-icon .mdc-button__icon,.trailing-icon .mdc-button__icon[dir=rtl]{margin-left:0;margin-right:8px}.slot-container{display:inline-flex;align-items:center;justify-content:center}.slot-container.flex{flex:auto}.mdc-button{flex:auto;overflow:hidden;padding-left:8px;padding-left:var(--mdc-button-horizontal-padding, 8px);padding-right:8px;padding-right:var(--mdc-button-horizontal-padding, 8px)}.mdc-button--raised{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-button-raised-box-shadow, 0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12))}.mdc-button--raised:hover,.mdc-button--raised:focus{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2), 0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-button-raised-box-shadow-hover, 0px 2px 4px -1px rgba(0, 0, 0, 0.2), 0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12))}.mdc-button--raised:active{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-button-raised-box-shadow-active, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}.mdc-button--raised:disabled{box-shadow:0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-button-raised-box-shadow-disabled, 0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12))}.mdc-button--raised,.mdc-button--unelevated{padding-left:16px;padding-left:var(--mdc-button-horizontal-padding, 16px);padding-right:16px;padding-right:var(--mdc-button-horizontal-padding, 16px)}.mdc-button--outlined{border-width:1px;border-width:var(--mdc-button-outline-width, 1px);padding-left:calc(16px - 1px);padding-left:calc(var(--mdc-button-horizontal-padding, 16px) - var(--mdc-button-outline-width, 1px));padding-right:calc(16px - 1px);padding-right:calc(var(--mdc-button-horizontal-padding, 16px) - var(--mdc-button-outline-width, 1px))}.mdc-button--outlined:not(:disabled){border-color:rgba(0, 0, 0, 0.12);border-color:var(--mdc-button-outline-color, rgba(0, 0, 0, 0.12))}.mdc-button--outlined mwc-ripple{top:calc(-1 * 1px);top:calc(-1 * var(--mdc-button-outline-width, 1px));left:calc(-1 * 1px);left:calc(-1 * var(--mdc-button-outline-width, 1px));right:initial;border-width:1px;border-width:var(--mdc-button-outline-width, 1px);border-style:solid;border-color:transparent}[dir=rtl] .mdc-button--outlined mwc-ripple,.mdc-button--outlined mwc-ripple[dir=rtl]{left:initial;right:calc(-1 * 1px);right:calc(-1 * var(--mdc-button-outline-width, 1px))}.mdc-button--dense{height:28px;margin-top:0;margin-bottom:0}.mdc-button--dense .mdc-button__touch{display:none}:host([disabled]){pointer-events:none}:host([disabled]) .mdc-button{color:rgba(0, 0, 0, 0.38);color:var(--mdc-button-disabled-ink-color, rgba(0, 0, 0, 0.38))}:host([disabled]) .mdc-button--raised,:host([disabled]) .mdc-button--unelevated{background-color:rgba(0, 0, 0, 0.12);background-color:var(--mdc-button-disabled-fill-color, rgba(0, 0, 0, 0.12))}:host([disabled]) .mdc-button--outlined{border-color:rgba(0, 0, 0, 0.12);border-color:var(--mdc-button-disabled-outline-color, rgba(0, 0, 0, 0.12))}`},82110:(t,e,n)=>{"use strict";n.d(e,{o:()=>i});const i=n(15652).iv`:host{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}`},70475:(t,e,n)=>{"use strict";var i=n(87480),r=n(15652),o=n(82110);let a=class extends r.oi{render(){return r.dy`<slot></slot>`}};a.styles=o.o,a=(0,i.gn)([(0,r.Mo)("mwc-icon")],a)},65660:(t,e,n)=>{"use strict";n(43437);const i=n(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content);var r=document.createElement("style");r.textContent="[hidden] { display: none !important; }",document.head.appendChild(r)},72986:(t,e,n)=>{"use strict";n.d(e,{z:()=>a});n(43437);var i=n(87156),r=n(74460),o=new Set;const a={properties:{_parentResizable:{type:Object,observer:"_parentResizableChanged"},_notifyingDescendant:{type:Boolean,value:!1}},listeners:{"iron-request-resize-notifications":"_onIronRequestResizeNotifications"},created:function(){this._interestedResizables=[],this._boundNotifyResize=this.notifyResize.bind(this),this._boundOnDescendantIronResize=this._onDescendantIronResize.bind(this)},attached:function(){this._requestResizeNotifications()},detached:function(){this._parentResizable?this._parentResizable.stopResizeNotificationsFor(this):(o.delete(this),window.removeEventListener("resize",this._boundNotifyResize)),this._parentResizable=null},notifyResize:function(){this.isAttached&&(this._interestedResizables.forEach((function(t){this.resizerShouldNotify(t)&&this._notifyDescendant(t)}),this),this._fireResize())},assignParentResizable:function(t){this._parentResizable&&this._parentResizable.stopResizeNotificationsFor(this),this._parentResizable=t,t&&-1===t._interestedResizables.indexOf(this)&&(t._interestedResizables.push(this),t._subscribeIronResize(this))},stopResizeNotificationsFor:function(t){var e=this._interestedResizables.indexOf(t);e>-1&&(this._interestedResizables.splice(e,1),this._unsubscribeIronResize(t))},_subscribeIronResize:function(t){t.addEventListener("iron-resize",this._boundOnDescendantIronResize)},_unsubscribeIronResize:function(t){t.removeEventListener("iron-resize",this._boundOnDescendantIronResize)},resizerShouldNotify:function(t){return!0},_onDescendantIronResize:function(t){this._notifyingDescendant?t.stopPropagation():r.my||this._fireResize()},_fireResize:function(){this.fire("iron-resize",null,{node:this,bubbles:!1})},_onIronRequestResizeNotifications:function(t){var e=(0,i.vz)(t).rootTarget;e!==this&&(e.assignParentResizable(this),this._notifyDescendant(e),t.stopPropagation())},_parentResizableChanged:function(t){t&&window.removeEventListener("resize",this._boundNotifyResize)},_notifyDescendant:function(t){this.isAttached&&(this._notifyingDescendant=!0,t.notifyResize(),this._notifyingDescendant=!1)},_requestResizeNotifications:function(){if(this.isAttached)if("loading"===document.readyState){var t=this._requestResizeNotifications.bind(this);document.addEventListener("readystatechange",(function e(){document.removeEventListener("readystatechange",e),t()}))}else this._findParent(),this._parentResizable?this._parentResizable._interestedResizables.forEach((function(t){t!==this&&t._findParent()}),this):(o.forEach((function(t){t!==this&&t._findParent()}),this),window.addEventListener("resize",this._boundNotifyResize),this.notifyResize())},_findParent:function(){this.assignParentResizable(null),this.fire("iron-request-resize-notifications",null,{node:this,bubbles:!0,cancelable:!0}),this._parentResizable?o.delete(this):o.add(this)}}},79332:(t,e,n)=>{"use strict";n.d(e,{a:()=>i});n(43437);const i={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,e){for(var n in e)t[n]=e[n]},_cloneConfig:function(t){var e={isClone:!0};return this._copyProperties(e,t),e},_getAnimationConfigRecursive:function(t,e,n){var i;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(i=t?this.animationConfig[t]:this.animationConfig,Array.isArray(i)||(i=[i]),i)for(var r,o=0;r=i[o];o++)if(r.animatable)r.animatable._getAnimationConfigRecursive(r.type||t,e,n);else if(r.id){var a=e[r.id];a?(a.isClone||(e[r.id]=this._cloneConfig(a),a=e[r.id]),this._copyProperties(a,r)):e[r.id]=r}else n.push(r)},getAnimationConfig:function(t){var e={},n=[];for(var i in this._getAnimationConfigRecursive(t,e,n),e)n.push(e[i]);return n}}},96540:(t,e,n)=>{"use strict";n.d(e,{t:()=>r});n(43437);const i={_configureAnimations:function(t){var e=[],n=[];if(t.length>0)for(let o,a=0;o=t[a];a++){let t=document.createElement(o.name);if(t.isNeonAnimation){let e=null;t.configure||(t.configure=function(t){return null}),e=t.configure(o),n.push({result:e,config:o,neonAnimation:t})}else console.warn(this.is+":",o.name,"not found!")}for(var i=0;i<n.length;i++){let t=n[i].result,o=n[i].config,a=n[i].neonAnimation;try{"function"!=typeof t.cancel&&(t=document.timeline.play(t))}catch(r){t=null,console.warn("Couldnt play","(",o.name,").",r)}t&&e.push({neonAnimation:a,config:o,animation:t})}return e},_shouldComplete:function(t){for(var e=!0,n=0;n<t.length;n++)if("finished"!=t[n].animation.playState){e=!1;break}return e},_complete:function(t){for(var e=0;e<t.length;e++)t[e].neonAnimation.complete(t[e].config);for(e=0;e<t.length;e++)t[e].animation.cancel()},playAnimation:function(t,e){var n=this.getAnimationConfig(t);if(n){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var i=this._configureAnimations(n);if(0!=i.length){this._active[t]=i;for(var r=0;r<i.length;r++)i[r].animation.onfinish=function(){this._shouldComplete(i)&&(this._complete(i),delete this._active[t],this.fire("neon-animation-finish",e,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",e,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var e=this._active[t];for(var n in e)e[n].animation.cancel()}this._active={}}},r=[n(79332).a,i]},51654:(t,e,n)=>{"use strict";n.d(e,{Z:()=>o,n:()=>a});n(43437);var i=n(75009),r=n(87156);const o={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,e){e&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var e=(0,r.vz)(t).path,n=0,i=e.indexOf(this);n<i;n++){var o=e[n];if(o.hasAttribute&&(o.hasAttribute("dialog-dismiss")||o.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(o.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},a=[i.$,o]},22626:(t,e,n)=>{"use strict";n(43437),n(65660);var i=n(51654),r=n(9672),o=n(50856);(0,r.k)({_template:o.d`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(i.Z)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},50808:(t,e,n)=>{"use strict";n(43437),n(65660),n(70019),n(54242);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content);var r=n(96540),o=n(51654),a=n(9672),s=n(50856);(0,a.k)({_template:s.d`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[o.n,r.t],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},25856:(t,e,n)=>{"use strict";n(43437),n(65660);var i=n(26110),r=n(98235),o=n(9672),a=n(87156),s=n(50856);(0,o.k)({_template:s.d`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[r.x,i.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(t){this.$.textarea.selectionStart=t},set selectionEnd(t){this.$.textarea.selectionEnd=t},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var t=this.$.textarea.validity.valid;return t&&(this.required&&""===this.value?t=!1:this.hasValidator()&&(t=r.x.validate.call(this,this.value))),this.invalid=!t,this.fire("iron-input-validate"),t},_bindValueChanged:function(t){this.value=t},_valueChanged:function(t){var e=this.textarea;e&&(e.value!==t&&(e.value=t||0===t?t:""),this.bindValue=t,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(t){var e=(0,a.vz)(t).path;this.value=e?e[0].value:t.target.value},_constrain:function(t){var e;for(t=t||[""],e=this.maxRows>0&&t.length>this.maxRows?t.slice(0,this.maxRows):t.slice(0);this.rows>0&&e.length<this.rows;)e.push("");return e.join("<br/>")+"&#160;"},_valueForMirror:function(){var t=this.textarea;if(t)return this.tokens=t&&t.value?t.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});n(2178),n(98121),n(65911);var l=n(21006),c=n(66668);(0,o.k)({_template:s.d`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[c.d0,l.V],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(t){this.$.input.textarea.selectionStart=t},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(t){this.$.input.textarea.selectionEnd=t},_ariaLabelledByChanged:function(t){this._focusableElement.setAttribute("aria-labelledby",t)},_ariaDescribedByChanged:function(t){this._focusableElement.setAttribute("aria-describedby",t)},get _focusableElement(){return this.inputElement.textarea}})},54242:(t,e,n)=>{"use strict";n(43437);const i=n(50856).d`
<custom-style>
  <style is="custom-style">
    html {

      --shadow-transition: {
        transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
      };

      --shadow-none: {
        box-shadow: none;
      };

      /* from http://codepen.io/shyndman/pen/c5394ddf2e8b2a5c9185904b57421cdb */

      --shadow-elevation-2dp: {
        box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),
                    0 1px 5px 0 rgba(0, 0, 0, 0.12),
                    0 3px 1px -2px rgba(0, 0, 0, 0.2);
      };

      --shadow-elevation-3dp: {
        box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.14),
                    0 1px 8px 0 rgba(0, 0, 0, 0.12),
                    0 3px 3px -2px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-4dp: {
        box-shadow: 0 4px 5px 0 rgba(0, 0, 0, 0.14),
                    0 1px 10px 0 rgba(0, 0, 0, 0.12),
                    0 2px 4px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-6dp: {
        box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14),
                    0 1px 18px 0 rgba(0, 0, 0, 0.12),
                    0 3px 5px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-8dp: {
        box-shadow: 0 8px 10px 1px rgba(0, 0, 0, 0.14),
                    0 3px 14px 2px rgba(0, 0, 0, 0.12),
                    0 5px 5px -3px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-12dp: {
        box-shadow: 0 12px 16px 1px rgba(0, 0, 0, 0.14),
                    0 4px 22px 3px rgba(0, 0, 0, 0.12),
                    0 6px 7px -4px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-16dp: {
        box-shadow: 0 16px 24px 2px rgba(0, 0, 0, 0.14),
                    0  6px 30px 5px rgba(0, 0, 0, 0.12),
                    0  8px 10px -5px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-24dp: {
        box-shadow: 0 24px 38px 3px rgba(0, 0, 0, 0.14),
                    0 9px 46px 8px rgba(0, 0, 0, 0.12),
                    0 11px 15px -7px rgba(0, 0, 0, 0.4);
      };
    }
  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},70019:(t,e,n)=>{"use strict";n(43437);const i=n(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},32333:(t,e,n)=>{"use strict";var i=n(15652);class r extends i.oi{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},readonly:{type:Boolean},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number},valueLabel:{type:String},lowLabel:{type:String},highLabel:{type:String}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.attachedListeners=!1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=((t=Math.min(this.max,Math.max(this.min,t)))-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let n=1;this._angleInside(270)||(n=Math.max(-t.y,-e.y));let i=1;this._angleInside(90)||(i=Math.max(t.y,e.y));let r=1;this._angleInside(180)||(r=Math.max(-t.x,-e.x));let o=1;return this._angleInside(0)||(o=Math.max(t.x,e.x)),{up:n,down:i,left:r,right:o,height:n+i,width:r+o}}_mouse2value(t){const e=t.type.startsWith("touch")?t.touches[0].clientX:t.clientX,n=t.type.startsWith("touch")?t.touches[0].clientY:t.clientY,i=this.shadowRoot.querySelector("svg").getBoundingClientRect(),r=this._boundaries,o=e-(i.left+r.left*i.width/r.width),a=n-(i.top+r.up*i.height/r.height),s=this._xy2angle(o,a);return this._angle2value(s)}dragStart(t){if(!this._showHandle||this.disabled)return;let e=t.target,n=void 0;if(this._rotation&&"focus"!==this._rotation.type)return;if(e.classList.contains("shadowpath"))if("touchstart"===t.type&&(n=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)e=this.shadowRoot.querySelector("#value");else{const n=this._mouse2value(t);e=Math.abs(n-this.low)<Math.abs(n-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(e.classList.contains("overflow")&&(e=e.nextElementSibling),!e.classList.contains("handle"))return;e.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const i="high"===e.id?this.low:this.min,r="low"===e.id?this.high:this.max;this._rotation={handle:e,min:i,max:r,start:this[e.id],type:t.type,cooldown:n},this.dragging=!0}_cleanupRotation(){const t=this._rotation.handle;t.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,t.blur()}dragEnd(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;this._cleanupRotation();let n=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]},bubbles:!0,composed:!0});this.dispatchEvent(n),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.coldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;t.preventDefault();const e=this._mouse2value(t);this._dragpos(e)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let n=new CustomEvent("value-changing",{detail:{[e.id]:t},bubbles:!0,composed:!0});this.dispatchEvent(n)}_keyStep(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"!==t.key&&"ArrowDown"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"!==t.key&&"ArrowUp"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step)),"Home"===t.key&&(t.preventDefault(),this._dragpos(this.min)),"End"===t.key&&(t.preventDefault(),this._dragpos(this.max))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(t){if(this.shadowRoot.querySelector(".slider")){const t=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(t&&t.strokeWidth){const e=parseFloat(t.strokeWidth);if(e>this.handleSize*this.handleZoom){const t=this._boundaries,n=`\n          ${e/2*Math.abs(t.up)}px\n          ${e/2*Math.abs(t.right)}px\n          ${e/2*Math.abs(t.down)}px\n          ${e/2*Math.abs(t.left)}px`;this.shadowRoot.querySelector("svg").style.margin=n}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=e*this._scale+"px"}));const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),n=Math.max(e.width,e.height);this._scale=2/n}}_renderArc(t,e){const n=e-t;return t=this._angle2xy(t),e=this._angle2xy(e+.001),`\n      M ${t.x} ${t.y}\n      A 1 1,\n        0,\n        ${n>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${e.x} ${e.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),n=this._angle2xy(e),r={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[t]||"";return i.YP`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${n.x} ${n.y}
          L ${n.x+.001} ${n.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${n.x} ${n.y}
          L ${n.x+.001} ${n.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[t]}
          aria-disabled=${this.disabled}
          aria-label=${r||""}
          />
        </g>
      `}render(){const t=this._boundaries;return i.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />

        </g>

        <g class="handles">
        ${this._showHandle?null!=this.low?this._reverseOrder?i.dy`${this._renderHandle("high")} ${this._renderHandle("low")}`:i.dy`${this._renderHandle("low")} ${this._renderHandle("high")}`:i.dy`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return i.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}customElements.define("round-slider",r)},60461:t=>{t.exports=function t(e){return Object.freeze(e),Object.getOwnPropertyNames(e).forEach((function(n){!e.hasOwnProperty(n)||null===e[n]||"object"!=typeof e[n]&&"function"!=typeof e[n]||Object.isFrozen(e[n])||t(e[n])})),e}},95282:(t,e,n)=>{"use strict";n.d(e,{_:()=>r,B:()=>o});var i=n(12902);const r=(t,e,n,r)=>{if(t[e])return t[e];let o,a=0,s=(0,i.M)();const l=()=>n(t).then((t=>s.setState(t,!0))),c=()=>l().catch((e=>{if(t.connected)throw e}));return t[e]={get state(){return s.state},refresh:l,subscribe(e){a++,1===a&&(r&&(o=r(t,s)),t.addEventListener("ready",c),c());const n=s.subscribe(e);return void 0!==s.state&&setTimeout((()=>e(s.state)),0),()=>{n(),a--,a||(o&&o.then((t=>{t()})),t.removeEventListener("ready",l))}}},t[e]},o=(t,e,n,i,o)=>r(i,t,e,n).subscribe(o)},23553:(t,e,n)=>{"use strict";n.d(e,{Pz:()=>r,U2:()=>o,iE:()=>a,PR:()=>s,_D:()=>l});var i=n(36007);const r=t=>t.sendMessagePromise(i.$q()),o=t=>t.sendMessagePromise(i.uZ()),a=t=>t.sendMessagePromise(i.vc()),s=t=>t.sendMessagePromise(i.EA()),l=(t,e,n,r)=>t.sendMessagePromise(i._D(e,n,r))},4915:(t,e,n)=>{"use strict";n.d(e,{wQ:()=>l,UE:()=>c,dL:()=>u,u5:()=>d});var i=n(95282),r=n(23553);function o(t,e){return void 0===t?null:{components:t.components.concat(e.data.component)}}const a=t=>(0,r.iE)(t),s=(t,e)=>Promise.all([t.subscribeEvents(e.action(o),"component_loaded"),t.subscribeEvents((()=>a(t).then((t=>e.setState(t,!0)))),"core_config_updated")]).then((t=>()=>t.forEach((t=>t())))),l=(t,e)=>(t=>(0,i._)(t,"_cnf",a,s))(t).subscribe(e),c="NOT_RUNNING",u="STARTING",d="RUNNING"},36007:(t,e,n)=>{"use strict";function i(t){return{type:"auth",access_token:t}}function r(){return{type:"get_states"}}function o(){return{type:"get_config"}}function a(){return{type:"get_services"}}function s(){return{type:"auth/current_user"}}function l(t,e,n){const i={type:"call_service",domain:t,service:e};return n&&(i.service_data=n),i}function c(t){const e={type:"subscribe_events"};return t&&(e.event_type=t),e}function u(t){return{type:"unsubscribe_events",subscription:t}}function d(){return{type:"ping"}}function p(t,e){return{type:"result",success:!1,error:{code:t,message:e}}}n.d(e,{I8:()=>i,$q:()=>r,vc:()=>o,uZ:()=>a,EA:()=>s,_D:()=>l,a:()=>c,Mt:()=>u,qE:()=>d,vU:()=>p})},12902:(t,e,n)=>{"use strict";n.d(e,{M:()=>i});const i=t=>{let e=[];function n(n,i){t=i?n:Object.assign(Object.assign({},t),n);let r=e;for(let e=0;e<r.length;e++)r[e](t)}return{get state(){return t},action(e){function i(t){n(t,!1)}return function(){let n=[t];for(let t=0;t<arguments.length;t++)n.push(arguments[t]);let r=e.apply(this,n);if(null!=r)return r instanceof Promise?r.then(i):i(r)}},setState:n,subscribe:t=>(e.push(t),()=>{!function(t){let n=[];for(let i=0;i<e.length;i++)e[i]===t?t=null:n.push(e[i]);e=n}(t)})}}},21602:(t,e,n)=>{"use strict";var i,r;function o(t){return t.type===i.literal}function a(t){return t.type===i.argument}function s(t){return t.type===i.number}function l(t){return t.type===i.date}function c(t){return t.type===i.time}function u(t){return t.type===i.select}function d(t){return t.type===i.plural}function p(t){return t.type===i.pound}function h(t){return t.type===i.tag}function f(t){return!(!t||"object"!=typeof t||0!==t.type)}function g(t){return!(!t||"object"!=typeof t||1!==t.type)}n.d(e,{ZP:()=>K}),function(t){t[t.literal=0]="literal",t[t.argument=1]="argument",t[t.number=2]="number",t[t.date=3]="date",t[t.time=4]="time",t[t.select=5]="select",t[t.plural=6]="plural",t[t.pound=7]="pound",t[t.tag=8]="tag"}(i||(i={})),function(t){t[t.number=0]="number",t[t.dateTime=1]="dateTime"}(r||(r={}));var m,b=(m=function(t,e){return(m=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])})(t,e)},function(t,e){function n(){this.constructor=t}m(t,e),t.prototype=null===e?Object.create(e):(n.prototype=e.prototype,new n)}),y=function(){return(y=Object.assign||function(t){for(var e,n=1,i=arguments.length;n<i;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)},x=function(t){function e(n,i,r,o){var a=t.call(this)||this;return a.message=n,a.expected=i,a.found=r,a.location=o,a.name="SyntaxError","function"==typeof Error.captureStackTrace&&Error.captureStackTrace(a,e),a}return b(e,t),e.buildMessage=function(t,e){function n(t){return t.charCodeAt(0).toString(16).toUpperCase()}function i(t){return t.replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(t){return"\\x0"+n(t)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(t){return"\\x"+n(t)}))}function r(t){return t.replace(/\\/g,"\\\\").replace(/\]/g,"\\]").replace(/\^/g,"\\^").replace(/-/g,"\\-").replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(t){return"\\x0"+n(t)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(t){return"\\x"+n(t)}))}function o(t){switch(t.type){case"literal":return'"'+i(t.text)+'"';case"class":var e=t.parts.map((function(t){return Array.isArray(t)?r(t[0])+"-"+r(t[1]):r(t)}));return"["+(t.inverted?"^":"")+e+"]";case"any":return"any character";case"end":return"end of input";case"other":return t.description}}return"Expected "+function(t){var e,n,i=t.map(o);if(i.sort(),i.length>0){for(e=1,n=1;e<i.length;e++)i[e-1]!==i[e]&&(i[n]=i[e],n++);i.length=n}switch(i.length){case 1:return i[0];case 2:return i[0]+" or "+i[1];default:return i.slice(0,-1).join(", ")+", or "+i[i.length-1]}}(t)+" but "+(((a=e)?'"'+i(a)+'"':"end of input")+" found.");var a},e}(Error);var v=function(t,e){e=void 0!==e?e:{};var n,r={},o={start:Gt},a=Gt,s=Tt("#",!1),l=Ht("tagElement"),c="<",u=Tt("<",!1),d="/>",p=Tt("/>",!1),h=">",f=Tt(">",!1),g=function(t){return ge.pop(),!0},m="</",b=Tt("</",!1),v=Ht("argumentElement"),_="{",w=Tt("{",!1),k="}",A=Tt("}",!1),C=Ht("numberSkeletonId"),R=/^['\/{}]/,z=Bt(["'","/","{","}"],!1,!1),E={type:"any"},$=Ht("numberSkeletonTokenOption"),S=Tt("/",!1),I=Ht("numberSkeletonToken"),O="::",D=Tt("::",!1),L=function(t){return ge.pop(),t.replace(/\s*$/,"")},N=",",M=Tt(",",!1),F="number",j=Tt("number",!1),P=function(t,e,n){return y({type:"number"===e?i.number:"date"===e?i.date:i.time,style:n&&n[2],value:t},ye())},T="'",B=Tt("'",!1),H=/^[^']/,q=Bt(["'"],!0,!1),V=/^[^a-zA-Z'{}]/,Z=Bt([["a","z"],["A","Z"],"'","{","}"],!0,!1),U=/^[a-zA-Z]/,G=Bt([["a","z"],["A","Z"]],!1,!1),K="date",W=Tt("date",!1),X="time",Y=Tt("time",!1),Q="plural",J=Tt("plural",!1),tt="selectordinal",et=Tt("selectordinal",!1),nt="offset:",it=Tt("offset:",!1),rt="select",ot=Tt("select",!1),at=Tt("=",!1),st=Ht("whitespace"),lt=/^[\t-\r \x85\xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]/,ct=Bt([["\t","\r"]," ",""," "," ",[" "," "],"\u2028","\u2029"," "," ","　"],!1,!1),ut=Ht("syntax pattern"),dt=/^[!-\/:-@[-\^`{-~\xA1-\xA7\xA9\xAB\xAC\xAE\xB0\xB1\xB6\xBB\xBF\xD7\xF7\u2010-\u2027\u2030-\u203E\u2041-\u2053\u2055-\u205E\u2190-\u245F\u2500-\u2775\u2794-\u2BFF\u2E00-\u2E7F\u3001-\u3003\u3008-\u3020\u3030\uFD3E\uFD3F\uFE45\uFE46]/,pt=Bt([["!","/"],[":","@"],["[","^"],"`",["{","~"],["¡","§"],"©","«","¬","®","°","±","¶","»","¿","×","÷",["‐","‧"],["‰","‾"],["⁁","⁓"],["⁕","⁞"],["←","⑟"],["─","❵"],["➔","⯿"],["⸀","⹿"],["、","〃"],["〈","〠"],"〰","﴾","﴿","﹅","﹆"],!1,!1),ht=Ht("optional whitespace"),ft=Ht("number"),gt="-",mt=Tt("-",!1),bt=(Ht("apostrophe"),Ht("double apostrophes")),yt="''",xt=Tt("''",!1),vt=Tt("\n",!1),_t=Ht("argNameOrNumber"),wt=Ht("validTag"),kt=Ht("argNumber"),At=Tt("0",!1),Ct=/^[1-9]/,Rt=Bt([["1","9"]],!1,!1),zt=/^[0-9]/,Et=Bt([["0","9"]],!1,!1),$t=Ht("argName"),St=Ht("tagName"),It=0,Ot=0,Dt=[{line:1,column:1}],Lt=0,Nt=[],Mt=0;if(void 0!==e.startRule){if(!(e.startRule in o))throw new Error("Can't start parsing from rule \""+e.startRule+'".');a=o[e.startRule]}function Ft(){return t.substring(Ot,It)}function jt(){return Vt(Ot,It)}function Pt(t,e){throw function(t,e){return new x(t,[],"",e)}(t,e=void 0!==e?e:Vt(Ot,It))}function Tt(t,e){return{type:"literal",text:t,ignoreCase:e}}function Bt(t,e,n){return{type:"class",parts:t,inverted:e,ignoreCase:n}}function Ht(t){return{type:"other",description:t}}function qt(e){var n,i=Dt[e];if(i)return i;for(n=e-1;!Dt[n];)n--;for(i={line:(i=Dt[n]).line,column:i.column};n<e;)10===t.charCodeAt(n)?(i.line++,i.column=1):i.column++,n++;return Dt[e]=i,i}function Vt(t,e){var n=qt(t),i=qt(e);return{start:{offset:t,line:n.line,column:n.column},end:{offset:e,line:i.line,column:i.column}}}function Zt(t){It<Lt||(It>Lt&&(Lt=It,Nt=[]),Nt.push(t))}function Ut(t,e,n){return new x(x.buildMessage(t,e),t,e,n)}function Gt(){return Kt()}function Kt(){var t,e;for(t=[],e=Wt();e!==r;)t.push(e),e=Wt();return t}function Wt(){var e;return(e=function(){var t,e;t=It,(e=Xt())!==r&&(Ot=t,n=e,e=y({type:i.literal,value:n},ye()));var n;return t=e}())===r&&(e=function(){var e,n,o,a;Mt++,e=It,123===t.charCodeAt(It)?(n=_,It++):(n=r,0===Mt&&Zt(w));n!==r&&ae()!==r&&(o=de())!==r&&ae()!==r?(125===t.charCodeAt(It)?(a=k,It++):(a=r,0===Mt&&Zt(A)),a!==r?(Ot=e,s=o,e=n=y({type:i.argument,value:s},ye())):(It=e,e=r)):(It=e,e=r);var s;Mt--,e===r&&(n=r,0===Mt&&Zt(v));return e}())===r&&(e=function(){var e;(e=function(){var e,n,i,o,a,s,l,c,u;e=It,123===t.charCodeAt(It)?(n=_,It++):(n=r,0===Mt&&Zt(w));n!==r&&ae()!==r&&(i=de())!==r&&ae()!==r?(44===t.charCodeAt(It)?(o=N,It++):(o=r,0===Mt&&Zt(M)),o!==r&&ae()!==r?(t.substr(It,6)===F?(a=F,It+=6):(a=r,0===Mt&&Zt(j)),a!==r&&ae()!==r?(s=It,44===t.charCodeAt(It)?(l=N,It++):(l=r,0===Mt&&Zt(M)),l!==r&&(c=ae())!==r&&(u=function(){var e,n,i;e=It,t.substr(It,2)===O?(n=O,It+=2):(n=r,0===Mt&&Zt(D));n!==r&&(i=function(){var t,e,n;if(t=It,e=[],(n=Jt())!==r)for(;n!==r;)e.push(n),n=Jt();else e=r;e!==r&&(Ot=t,e=y({type:0,tokens:e},ye()));return t=e}())!==r?(Ot=e,e=n=i):(It=e,e=r);e===r&&(e=It,Ot=It,ge.push("numberArgStyle"),(n=(n=!0)?void 0:r)!==r&&(i=Xt())!==r?(Ot=e,e=n=L(i)):(It=e,e=r));return e}())!==r?s=l=[l,c,u]:(It=s,s=r),s===r&&(s=null),s!==r&&(l=ae())!==r?(125===t.charCodeAt(It)?(c=k,It++):(c=r,0===Mt&&Zt(A)),c!==r?(Ot=e,e=n=P(i,a,s)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r);return e}())===r&&(e=function(){var e,n,i,o,a,s,l,c,u;e=It,123===t.charCodeAt(It)?(n=_,It++):(n=r,0===Mt&&Zt(w));n!==r&&ae()!==r&&(i=de())!==r&&ae()!==r?(44===t.charCodeAt(It)?(o=N,It++):(o=r,0===Mt&&Zt(M)),o!==r&&ae()!==r?(t.substr(It,4)===K?(a=K,It+=4):(a=r,0===Mt&&Zt(W)),a===r&&(t.substr(It,4)===X?(a=X,It+=4):(a=r,0===Mt&&Zt(Y))),a!==r&&ae()!==r?(s=It,44===t.charCodeAt(It)?(l=N,It++):(l=r,0===Mt&&Zt(M)),l!==r&&(c=ae())!==r&&(u=function(){var e,n,i;e=It,t.substr(It,2)===O?(n=O,It+=2):(n=r,0===Mt&&Zt(D));n!==r&&(i=function(){var e,n,i,o;e=It,n=It,i=[],(o=te())===r&&(o=ee());if(o!==r)for(;o!==r;)i.push(o),(o=te())===r&&(o=ee());else i=r;n=i!==r?t.substring(n,It):i;n!==r&&(Ot=e,n=y({type:1,pattern:n},ye()));return e=n}())!==r?(Ot=e,e=n=i):(It=e,e=r);e===r&&(e=It,Ot=It,ge.push("dateOrTimeArgStyle"),(n=(n=!0)?void 0:r)!==r&&(i=Xt())!==r?(Ot=e,e=n=L(i)):(It=e,e=r));return e}())!==r?s=l=[l,c,u]:(It=s,s=r),s===r&&(s=null),s!==r&&(l=ae())!==r?(125===t.charCodeAt(It)?(c=k,It++):(c=r,0===Mt&&Zt(A)),c!==r?(Ot=e,e=n=P(i,a,s)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r);return e}());return e}())===r&&(e=function(){var e,n,o,a,s,l,c,u,d,p,h;e=It,123===t.charCodeAt(It)?(n=_,It++):(n=r,0===Mt&&Zt(w));if(n!==r)if(ae()!==r)if((o=de())!==r)if(ae()!==r)if(44===t.charCodeAt(It)?(a=N,It++):(a=r,0===Mt&&Zt(M)),a!==r)if(ae()!==r)if(t.substr(It,6)===Q?(s=Q,It+=6):(s=r,0===Mt&&Zt(J)),s===r&&(t.substr(It,13)===tt?(s=tt,It+=13):(s=r,0===Mt&&Zt(et))),s!==r)if(ae()!==r)if(44===t.charCodeAt(It)?(l=N,It++):(l=r,0===Mt&&Zt(M)),l!==r)if(ae()!==r)if(c=It,t.substr(It,7)===nt?(u=nt,It+=7):(u=r,0===Mt&&Zt(it)),u!==r&&(d=ae())!==r&&(p=se())!==r?c=u=[u,d,p]:(It=c,c=r),c===r&&(c=null),c!==r)if((u=ae())!==r){if(d=[],(p=ie())!==r)for(;p!==r;)d.push(p),p=ie();else d=r;d!==r&&(p=ae())!==r?(125===t.charCodeAt(It)?(h=k,It++):(h=r,0===Mt&&Zt(A)),h!==r?(Ot=e,e=n=function(t,e,n,r){return y({type:i.plural,pluralType:"plural"===e?"cardinal":"ordinal",value:t,offset:n?n[2]:0,options:r.reduce((function(t,e){var n=e.id,i=e.value,r=e.location;return n in t&&Pt('Duplicate option "'+n+'" in plural element: "'+Ft()+'"',jt()),t[n]={value:i,location:r},t}),{})},ye())}(o,s,c,d)):(It=e,e=r)):(It=e,e=r)}else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;return e}())===r&&(e=function(){var e,n,o,a,s,l,c,u,d;e=It,123===t.charCodeAt(It)?(n=_,It++):(n=r,0===Mt&&Zt(w));if(n!==r)if(ae()!==r)if((o=de())!==r)if(ae()!==r)if(44===t.charCodeAt(It)?(a=N,It++):(a=r,0===Mt&&Zt(M)),a!==r)if(ae()!==r)if(t.substr(It,6)===rt?(s=rt,It+=6):(s=r,0===Mt&&Zt(ot)),s!==r)if(ae()!==r)if(44===t.charCodeAt(It)?(l=N,It++):(l=r,0===Mt&&Zt(M)),l!==r)if(ae()!==r){if(c=[],(u=ne())!==r)for(;u!==r;)c.push(u),u=ne();else c=r;c!==r&&(u=ae())!==r?(125===t.charCodeAt(It)?(d=k,It++):(d=r,0===Mt&&Zt(A)),d!==r?(Ot=e,e=n=function(t,e){return y({type:i.select,value:t,options:e.reduce((function(t,e){var n=e.id,i=e.value,r=e.location;return n in t&&Pt('Duplicate option "'+n+'" in select element: "'+Ft()+'"',jt()),t[n]={value:i,location:r},t}),{})},ye())}(o,c)):(It=e,e=r)):(It=e,e=r)}else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;else It=e,e=r;return e}())===r&&(e=function(){var e,n,o,a,s,x;Mt++,e=It,n=It,60===t.charCodeAt(It)?(o="<",It++):(o=r,0===Mt&&Zt(u));o!==r&&(a=pe())!==r&&(s=ae())!==r?(t.substr(It,2)===d?(x=d,It+=2):(x=r,0===Mt&&Zt(p)),x!==r?n=o=[o,a,s,x]:(It=n,n=r)):(It=n,n=r);n!==r&&(Ot=e,v=n,n=y({type:i.literal,value:v.join("")},ye()));var v;(e=n)===r&&(e=It,(n=function(){var e,n,i,o;e=It,60===t.charCodeAt(It)?(n=c,It++):(n=r,0===Mt&&Zt(u));n!==r?(Ot=It,ge.push("openingTag"),(!0?void 0:r)!==r&&(i=pe())!==r?(62===t.charCodeAt(It)?(o=">",It++):(o=r,0===Mt&&Zt(f)),o!==r?(Ot=It,(g()?void 0:r)!==r?(Ot=e,e=n=i):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r);return e}())!==r&&(o=Kt())!==r&&(a=function(){var e,n,i,o;e=It,t.substr(It,2)===m?(n=m,It+=2):(n=r,0===Mt&&Zt(b));n!==r?(Ot=It,ge.push("closingTag"),(!0?void 0:r)!==r&&(i=pe())!==r?(62===t.charCodeAt(It)?(o=h,It++):(o=r,0===Mt&&Zt(f)),o!==r?(Ot=It,(g()?void 0:r)!==r?(Ot=e,e=n=i):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r);return e}())!==r?(Ot=e,w=o,(_=n)!==(k=a)&&Pt('Mismatch tag "'+_+'" !== "'+k+'"',jt()),e=n=y({type:i.tag,value:_,children:w},ye())):(It=e,e=r));var _,w,k;Mt--,e===r&&(n=r,0===Mt&&Zt(l));return e}())===r&&(e=function(){var e,n;e=It,35===t.charCodeAt(It)?(n="#",It++):(n=r,0===Mt&&Zt(s));n!==r&&(Ot=e,n=y({type:i.pound},ye()));return e=n}()),e}function Xt(){var t,e,n;if(t=It,e=[],(n=le())===r&&(n=ce())===r&&(n=ue()),n!==r)for(;n!==r;)e.push(n),(n=le())===r&&(n=ce())===r&&(n=ue());else e=r;return e!==r&&(Ot=t,e=e.join("")),t=e}function Yt(){var e,n,i,o,a;if(Mt++,e=It,n=[],i=It,o=It,Mt++,(a=re())===r&&(R.test(t.charAt(It))?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(z))),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r),i!==r)for(;i!==r;)n.push(i),i=It,o=It,Mt++,(a=re())===r&&(R.test(t.charAt(It))?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(z))),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r);else n=r;return e=n!==r?t.substring(e,It):n,Mt--,e===r&&(n=r,0===Mt&&Zt(C)),e}function Qt(){var e,n,i;return Mt++,e=It,47===t.charCodeAt(It)?(n="/",It++):(n=r,0===Mt&&Zt(S)),n!==r&&(i=Yt())!==r?(Ot=e,e=n=i):(It=e,e=r),Mt--,e===r&&(n=r,0===Mt&&Zt($)),e}function Jt(){var t,e,n,i;if(Mt++,t=It,ae()!==r)if((e=Yt())!==r){for(n=[],i=Qt();i!==r;)n.push(i),i=Qt();n!==r?(Ot=t,t=function(t,e){return{stem:t,options:e}}(e,n)):(It=t,t=r)}else It=t,t=r;else It=t,t=r;return Mt--,t===r&&(r,0===Mt&&Zt(I)),t}function te(){var e,n,i,o;if(e=It,39===t.charCodeAt(It)?(n=T,It++):(n=r,0===Mt&&Zt(B)),n!==r){if(i=[],(o=le())===r&&(H.test(t.charAt(It))?(o=t.charAt(It),It++):(o=r,0===Mt&&Zt(q))),o!==r)for(;o!==r;)i.push(o),(o=le())===r&&(H.test(t.charAt(It))?(o=t.charAt(It),It++):(o=r,0===Mt&&Zt(q)));else i=r;i!==r?(39===t.charCodeAt(It)?(o=T,It++):(o=r,0===Mt&&Zt(B)),o!==r?e=n=[n,i,o]:(It=e,e=r)):(It=e,e=r)}else It=e,e=r;if(e===r)if(e=[],(n=le())===r&&(V.test(t.charAt(It))?(n=t.charAt(It),It++):(n=r,0===Mt&&Zt(Z))),n!==r)for(;n!==r;)e.push(n),(n=le())===r&&(V.test(t.charAt(It))?(n=t.charAt(It),It++):(n=r,0===Mt&&Zt(Z)));else e=r;return e}function ee(){var e,n;if(e=[],U.test(t.charAt(It))?(n=t.charAt(It),It++):(n=r,0===Mt&&Zt(G)),n!==r)for(;n!==r;)e.push(n),U.test(t.charAt(It))?(n=t.charAt(It),It++):(n=r,0===Mt&&Zt(G));else e=r;return e}function ne(){var e,n,i,o,a,s,l;return e=It,ae()!==r&&(n=fe())!==r&&ae()!==r?(123===t.charCodeAt(It)?(i=_,It++):(i=r,0===Mt&&Zt(w)),i!==r?(Ot=It,ge.push("select"),(!0?void 0:r)!==r&&(o=Kt())!==r?(125===t.charCodeAt(It)?(a=k,It++):(a=r,0===Mt&&Zt(A)),a!==r?(Ot=e,s=n,l=o,ge.pop(),e=y({id:s,value:l},ye())):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r),e}function ie(){var e,n,i,o,a,s,l;return e=It,ae()!==r&&(n=function(){var e,n,i,o;return e=It,n=It,61===t.charCodeAt(It)?(i="=",It++):(i=r,0===Mt&&Zt(at)),i!==r&&(o=se())!==r?n=i=[i,o]:(It=n,n=r),(e=n!==r?t.substring(e,It):n)===r&&(e=fe()),e}())!==r&&ae()!==r?(123===t.charCodeAt(It)?(i=_,It++):(i=r,0===Mt&&Zt(w)),i!==r?(Ot=It,ge.push("plural"),(!0?void 0:r)!==r&&(o=Kt())!==r?(125===t.charCodeAt(It)?(a=k,It++):(a=r,0===Mt&&Zt(A)),a!==r?(Ot=e,s=n,l=o,ge.pop(),e=y({id:s,value:l},ye())):(It=e,e=r)):(It=e,e=r)):(It=e,e=r)):(It=e,e=r),e}function re(){var e;return Mt++,lt.test(t.charAt(It))?(e=t.charAt(It),It++):(e=r,0===Mt&&Zt(ct)),Mt--,e===r&&(r,0===Mt&&Zt(st)),e}function oe(){var e;return Mt++,dt.test(t.charAt(It))?(e=t.charAt(It),It++):(e=r,0===Mt&&Zt(pt)),Mt--,e===r&&(r,0===Mt&&Zt(ut)),e}function ae(){var e,n,i;for(Mt++,e=It,n=[],i=re();i!==r;)n.push(i),i=re();return e=n!==r?t.substring(e,It):n,Mt--,e===r&&(n=r,0===Mt&&Zt(ht)),e}function se(){var e,n,i,o,a;return Mt++,e=It,45===t.charCodeAt(It)?(n="-",It++):(n=r,0===Mt&&Zt(mt)),n===r&&(n=null),n!==r&&(i=he())!==r?(Ot=e,o=n,e=n=(a=i)?o?-a:a:0):(It=e,e=r),Mt--,e===r&&(n=r,0===Mt&&Zt(ft)),e}function le(){var e,n;return Mt++,e=It,t.substr(It,2)===yt?(n=yt,It+=2):(n=r,0===Mt&&Zt(xt)),n!==r&&(Ot=e,n="'"),Mt--,(e=n)===r&&(n=r,0===Mt&&Zt(bt)),e}function ce(){var e,n,i,o,a,s;if(e=It,39===t.charCodeAt(It)?(n=T,It++):(n=r,0===Mt&&Zt(B)),n!==r)if((i=function(){var e,n,i,o;e=It,n=It,t.length>It?(i=t.charAt(It),It++):(i=r,0===Mt&&Zt(E));i!==r?(Ot=It,(o=(o="<"===(a=i)||">"===a||"{"===a||"}"===a||be()&&"#"===a)?void 0:r)!==r?n=i=[i,o]:(It=n,n=r)):(It=n,n=r);var a;e=n!==r?t.substring(e,It):n;return e}())!==r){for(o=It,a=[],t.substr(It,2)===yt?(s=yt,It+=2):(s=r,0===Mt&&Zt(xt)),s===r&&(H.test(t.charAt(It))?(s=t.charAt(It),It++):(s=r,0===Mt&&Zt(q)));s!==r;)a.push(s),t.substr(It,2)===yt?(s=yt,It+=2):(s=r,0===Mt&&Zt(xt)),s===r&&(H.test(t.charAt(It))?(s=t.charAt(It),It++):(s=r,0===Mt&&Zt(q)));(o=a!==r?t.substring(o,It):a)!==r?(39===t.charCodeAt(It)?(a=T,It++):(a=r,0===Mt&&Zt(B)),a===r&&(a=null),a!==r?(Ot=e,e=n=i+o.replace("''","'")):(It=e,e=r)):(It=e,e=r)}else It=e,e=r;else It=e,e=r;return e}function ue(){var e,n,i,o,a;return e=It,n=It,t.length>It?(i=t.charAt(It),It++):(i=r,0===Mt&&Zt(E)),i!==r?(Ot=It,(o=(o=!("<"===(a=i)||"{"===a||be()&&"#"===a||me()&&"}"===a||me()&&">"===a))?void 0:r)!==r?n=i=[i,o]:(It=n,n=r)):(It=n,n=r),n===r&&(10===t.charCodeAt(It)?(n="\n",It++):(n=r,0===Mt&&Zt(vt))),e=n!==r?t.substring(e,It):n}function de(){var e,n;return Mt++,e=It,(n=he())===r&&(n=fe()),e=n!==r?t.substring(e,It):n,Mt--,e===r&&(n=r,0===Mt&&Zt(_t)),e}function pe(){var e,n;return Mt++,e=It,(n=he())===r&&(n=function(){var e,n,i,o,a;Mt++,e=It,n=[],45===t.charCodeAt(It)?(i=gt,It++):(i=r,0===Mt&&Zt(mt));i===r&&(i=It,o=It,Mt++,(a=re())===r&&(a=oe()),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r));if(i!==r)for(;i!==r;)n.push(i),45===t.charCodeAt(It)?(i=gt,It++):(i=r,0===Mt&&Zt(mt)),i===r&&(i=It,o=It,Mt++,(a=re())===r&&(a=oe()),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r));else n=r;e=n!==r?t.substring(e,It):n;Mt--,e===r&&(n=r,0===Mt&&Zt(St));return e}()),e=n!==r?t.substring(e,It):n,Mt--,e===r&&(n=r,0===Mt&&Zt(wt)),e}function he(){var e,n,i,o,a;if(Mt++,e=It,48===t.charCodeAt(It)?(n="0",It++):(n=r,0===Mt&&Zt(At)),n!==r&&(Ot=e,n=0),(e=n)===r){if(e=It,n=It,Ct.test(t.charAt(It))?(i=t.charAt(It),It++):(i=r,0===Mt&&Zt(Rt)),i!==r){for(o=[],zt.test(t.charAt(It))?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(Et));a!==r;)o.push(a),zt.test(t.charAt(It))?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(Et));o!==r?n=i=[i,o]:(It=n,n=r)}else It=n,n=r;n!==r&&(Ot=e,n=parseInt(n.join(""),10)),e=n}return Mt--,e===r&&(n=r,0===Mt&&Zt(kt)),e}function fe(){var e,n,i,o,a;if(Mt++,e=It,n=[],i=It,o=It,Mt++,(a=re())===r&&(a=oe()),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r),i!==r)for(;i!==r;)n.push(i),i=It,o=It,Mt++,(a=re())===r&&(a=oe()),Mt--,a===r?o=void 0:(It=o,o=r),o!==r?(t.length>It?(a=t.charAt(It),It++):(a=r,0===Mt&&Zt(E)),a!==r?i=o=[o,a]:(It=i,i=r)):(It=i,i=r);else n=r;return e=n!==r?t.substring(e,It):n,Mt--,e===r&&(n=r,0===Mt&&Zt($t)),e}var ge=["root"];function me(){return ge.length>1}function be(){return"plural"===ge[ge.length-1]}function ye(){return e&&e.captureLocation?{location:jt()}:{}}if((n=a())!==r&&It===t.length)return n;throw n!==r&&It<t.length&&Zt({type:"end"}),Ut(Nt,Lt<t.length?t.charAt(Lt):null,Lt<t.length?Vt(Lt,Lt+1):Vt(Lt,Lt))},_=function(){for(var t=0,e=0,n=arguments.length;e<n;e++)t+=arguments[e].length;var i=Array(t),r=0;for(e=0;e<n;e++)for(var o=arguments[e],a=0,s=o.length;a<s;a++,r++)i[r]=o[a];return i},w=/(^|[^\\])#/g;function k(t){t.forEach((function(t){(d(t)||u(t))&&Object.keys(t.options).forEach((function(e){for(var n,i=t.options[e],r=-1,a=void 0,s=0;s<i.value.length;s++){var l=i.value[s];if(o(l)&&w.test(l.value)){r=s,a=l;break}}if(a){var c=a.value.replace(w,"$1{"+t.value+", number}"),u=v(c);(n=i.value).splice.apply(n,_([r,1],u))}k(i.value)}))}))}function A(t,e){var n=v(t,e);return e&&!1===e.normalizeHashtagInPlural||k(n),n}var C=function(){for(var t=0,e=0,n=arguments.length;e<n;e++)t+=arguments[e].length;var i=Array(t),r=0;for(e=0;e<n;e++)for(var o=arguments[e],a=0,s=o.length;a<s;a++,r++)i[r]=o[a];return i};function R(t){return JSON.stringify(t.map((function(t){return t&&"object"==typeof t?(e=t,Object.keys(e).sort().map((function(t){var n;return(n={})[t]=e[t],n}))):t;var e})))}const z=function(t,e){return void 0===e&&(e={}),function(){for(var n,i=[],r=0;r<arguments.length;r++)i[r]=arguments[r];var o=R(i),a=o&&e[o];return a||(a=new((n=t).bind.apply(n,C([void 0],i))),o&&(e[o]=a)),a}};var E=function(){return(E=Object.assign||function(t){for(var e,n=1,i=arguments.length;n<i;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)},$=/(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;function S(t){var e={};return t.replace($,(function(t){var n=t.length;switch(t[0]){case"G":e.era=4===n?"long":5===n?"narrow":"short";break;case"y":e.year=2===n?"2-digit":"numeric";break;case"Y":case"u":case"U":case"r":throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");case"q":case"Q":throw new RangeError("`q/Q` (quarter) patterns are not supported");case"M":case"L":e.month=["numeric","2-digit","short","long","narrow"][n-1];break;case"w":case"W":throw new RangeError("`w/W` (week) patterns are not supported");case"d":e.day=["numeric","2-digit"][n-1];break;case"D":case"F":case"g":throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");case"E":e.weekday=4===n?"short":5===n?"narrow":"short";break;case"e":if(n<4)throw new RangeError("`e..eee` (weekday) patterns are not supported");e.weekday=["short","long","narrow","short"][n-4];break;case"c":if(n<4)throw new RangeError("`c..ccc` (weekday) patterns are not supported");e.weekday=["short","long","narrow","short"][n-4];break;case"a":e.hour12=!0;break;case"b":case"B":throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");case"h":e.hourCycle="h12",e.hour=["numeric","2-digit"][n-1];break;case"H":e.hourCycle="h23",e.hour=["numeric","2-digit"][n-1];break;case"K":e.hourCycle="h11",e.hour=["numeric","2-digit"][n-1];break;case"k":e.hourCycle="h24",e.hour=["numeric","2-digit"][n-1];break;case"j":case"J":case"C":throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");case"m":e.minute=["numeric","2-digit"][n-1];break;case"s":e.second=["numeric","2-digit"][n-1];break;case"S":case"A":throw new RangeError("`S/A` (second) pattenrs are not supported, use `s` instead");case"z":e.timeZoneName=n<4?"short":"long";break;case"Z":case"O":case"v":case"V":case"X":case"x":throw new RangeError("`Z/O/v/V/X/x` (timeZone) pattenrs are not supported, use `z` instead")}return""})),e}var I=/^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g,O=/^(@+)?(\+|#+)?$/g;function D(t){var e={};return t.replace(O,(function(t,n,i){return"string"!=typeof i?(e.minimumSignificantDigits=n.length,e.maximumSignificantDigits=n.length):"+"===i?e.minimumSignificantDigits=n.length:"#"===n[0]?e.maximumSignificantDigits=n.length:(e.minimumSignificantDigits=n.length,e.maximumSignificantDigits=n.length+("string"==typeof i?i.length:0)),""})),e}function L(t){switch(t){case"sign-auto":return{signDisplay:"auto"};case"sign-accounting":return{currencySign:"accounting"};case"sign-always":return{signDisplay:"always"};case"sign-accounting-always":return{signDisplay:"always",currencySign:"accounting"};case"sign-except-zero":return{signDisplay:"exceptZero"};case"sign-accounting-except-zero":return{signDisplay:"exceptZero",currencySign:"accounting"};case"sign-never":return{signDisplay:"never"}}}function N(t){var e=L(t);return e||{}}function M(t){for(var e={},n=0,i=t;n<i.length;n++){var r=i[n];switch(r.stem){case"percent":e.style="percent";continue;case"currency":e.style="currency",e.currency=r.options[0];continue;case"group-off":e.useGrouping=!1;continue;case"precision-integer":case".":e.maximumFractionDigits=0;continue;case"measure-unit":e.style="unit",e.unit=r.options[0].replace(/^(.*?)-/,"");continue;case"compact-short":e.notation="compact",e.compactDisplay="short";continue;case"compact-long":e.notation="compact",e.compactDisplay="long";continue;case"scientific":e=E(E(E({},e),{notation:"scientific"}),r.options.reduce((function(t,e){return E(E({},t),N(e))}),{}));continue;case"engineering":e=E(E(E({},e),{notation:"engineering"}),r.options.reduce((function(t,e){return E(E({},t),N(e))}),{}));continue;case"notation-simple":e.notation="standard";continue;case"unit-width-narrow":e.currencyDisplay="narrowSymbol",e.unitDisplay="narrow";continue;case"unit-width-short":e.currencyDisplay="code",e.unitDisplay="short";continue;case"unit-width-full-name":e.currencyDisplay="name",e.unitDisplay="long";continue;case"unit-width-iso-code":e.currencyDisplay="symbol";continue}if(I.test(r.stem)){if(r.options.length>1)throw new RangeError("Fraction-precision stems only accept a single optional option");r.stem.replace(I,(function(t,n,i,r,o,a){return"*"===i?e.minimumFractionDigits=n.length:r&&"#"===r[0]?e.maximumFractionDigits=r.length:o&&a?(e.minimumFractionDigits=o.length,e.maximumFractionDigits=o.length+a.length):(e.minimumFractionDigits=n.length,e.maximumFractionDigits=n.length),""})),r.options.length&&(e=E(E({},e),D(r.options[0])))}else if(O.test(r.stem))e=E(E({},e),D(r.stem));else{var o=L(r.stem);o&&(e=E(E({},e),o))}}return e}var F,j=function(){var t=function(e,n){return(t=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])})(e,n)};return function(e,n){function i(){this.constructor=e}t(e,n),e.prototype=null===n?Object.create(n):(i.prototype=n.prototype,new i)}}();!function(t){t.MISSING_VALUE="MISSING_VALUE",t.INVALID_VALUE="INVALID_VALUE",t.MISSING_INTL_API="MISSING_INTL_API"}(F||(F={}));var P,T=function(t){function e(e,n,i){var r=t.call(this,e)||this;return r.code=n,r.originalMessage=i,r}return j(e,t),e.prototype.toString=function(){return"[formatjs Error: "+this.code+"] "+this.message},e}(Error),B=function(t){function e(e,n,i,r){return t.call(this,'Invalid values for "'+e+'": "'+n+'". Options are "'+Object.keys(i).join('", "')+'"',"INVALID_VALUE",r)||this}return j(e,t),e}(T),H=function(t){function e(e,n,i){return t.call(this,'Value for "'+e+'" must be of type '+n,"INVALID_VALUE",i)||this}return j(e,t),e}(T),q=function(t){function e(e,n){return t.call(this,'The intl string context variable "'+e+'" was not provided to the string "'+n+'"',"MISSING_VALUE",n)||this}return j(e,t),e}(T);function V(t){return"function"==typeof t}function Z(t,e,n,i,r,m,b){if(1===t.length&&o(t[0]))return[{type:0,value:t[0].value}];for(var y=[],x=0,v=t;x<v.length;x++){var _=v[x];if(o(_))y.push({type:0,value:_.value});else if(p(_))"number"==typeof m&&y.push({type:0,value:n.getNumberFormat(e).format(m)});else{var w=_.value;if(!r||!(w in r))throw new q(w,b);var k=r[w];if(a(_))k&&"string"!=typeof k&&"number"!=typeof k||(k="string"==typeof k||"number"==typeof k?String(k):""),y.push({type:"string"==typeof k?0:1,value:k});else if(l(_)){var A="string"==typeof _.style?i.date[_.style]:g(_.style)?S(_.style.pattern):void 0;y.push({type:0,value:n.getDateTimeFormat(e,A).format(k)})}else if(c(_)){A="string"==typeof _.style?i.time[_.style]:g(_.style)?S(_.style.pattern):void 0;y.push({type:0,value:n.getDateTimeFormat(e,A).format(k)})}else if(s(_)){A="string"==typeof _.style?i.number[_.style]:f(_.style)?M(_.style.tokens):void 0;y.push({type:0,value:n.getNumberFormat(e,A).format(k)})}else{if(h(_)){var C=_.children,R=_.value,z=r[R];if(!V(z))throw new H(R,"function",b);var E=Z(C,e,n,i,r),$=z.apply(void 0,E.map((function(t){return t.value})));Array.isArray($)||($=[$]),y.push.apply(y,$.map((function(t){return{type:"string"==typeof t?0:1,value:t}})))}if(u(_)){if(!(I=_.options[k]||_.options.other))throw new B(_.value,k,Object.keys(_.options),b);y.push.apply(y,Z(I.value,e,n,i,r))}else if(d(_)){var I;if(!(I=_.options["="+k])){if(!Intl.PluralRules)throw new T('Intl.PluralRules is not available in this environment.\nTry polyfilling it using "@formatjs/intl-pluralrules"\n',"MISSING_INTL_API",b);var O=n.getPluralRules(e,{type:_.pluralType}).select(k-(_.offset||0));I=_.options[O]||_.options.other}if(!I)throw new B(_.value,k,Object.keys(_.options),b);y.push.apply(y,Z(I.value,e,n,i,r,k-(_.offset||0)))}else;}}}return function(t){return t.length<2?t:t.reduce((function(t,e){var n=t[t.length-1];return n&&0===n.type&&0===e.type?n.value+=e.value:t.push(e),t}),[])}(y)}!function(t){t[t.literal=0]="literal",t[t.object=1]="object"}(P||(P={}));var U=function(){return(U=Object.assign||function(t){for(var e,n=1,i=arguments.length;n<i;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)};function G(t,e){return e?Object.keys(t).reduce((function(n,i){var r,o;return n[i]=(r=t[i],(o=e[i])?U(U(U({},r||{}),o||{}),Object.keys(r).reduce((function(t,e){return t[e]=U(U({},r[e]),o[e]||{}),t}),{})):r),n}),U({},t)):t}const K=function(){function t(e,n,i,r){var o,a=this;if(void 0===n&&(n=t.defaultLocale),this.formatterCache={number:{},dateTime:{},pluralRules:{}},this.format=function(t){var e=a.formatToParts(t);if(1===e.length)return e[0].value;var n=e.reduce((function(t,e){return t.length&&0===e.type&&"string"==typeof t[t.length-1]?t[t.length-1]+=e.value:t.push(e.value),t}),[]);return n.length<=1?n[0]||"":n},this.formatToParts=function(t){return Z(a.ast,a.locales,a.formatters,a.formats,t,void 0,a.message)},this.resolvedOptions=function(){return{locale:Intl.NumberFormat.supportedLocalesOf(a.locales)[0]}},this.getAst=function(){return a.ast},"string"==typeof e){if(this.message=e,!t.__parse)throw new TypeError("IntlMessageFormat.__parse must be set to process `message` of type `string`");this.ast=t.__parse(e,{normalizeHashtagInPlural:!1})}else this.ast=e;if(!Array.isArray(this.ast))throw new TypeError("A message must be provided as a String or AST.");this.formats=G(t.formats,i),this.locales=n,this.formatters=r&&r.formatters||(void 0===(o=this.formatterCache)&&(o={number:{},dateTime:{},pluralRules:{}}),{getNumberFormat:z(Intl.NumberFormat,o.number),getDateTimeFormat:z(Intl.DateTimeFormat,o.dateTime),getPluralRules:z(Intl.PluralRules,o.pluralRules)})}return Object.defineProperty(t,"defaultLocale",{get:function(){return t.memoizedDefaultLocale||(t.memoizedDefaultLocale=(new Intl.NumberFormat).resolvedOptions().locale),t.memoizedDefaultLocale},enumerable:!0,configurable:!0}),t.memoizedDefaultLocale=null,t.__parse=A,t.formats={number:{currency:{style:"currency"},percent:{style:"percent"}},date:{short:{month:"numeric",day:"numeric",year:"2-digit"},medium:{month:"short",day:"numeric",year:"numeric"},long:{month:"long",day:"numeric",year:"numeric"},full:{weekday:"long",month:"long",day:"numeric",year:"numeric"}},time:{short:{hour:"numeric",minute:"numeric"},medium:{hour:"numeric",minute:"numeric",second:"numeric"},long:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"},full:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"}}},t}()}}]);
//# sourceMappingURL=chunk.7bbf9684d798bb864b96.js.map