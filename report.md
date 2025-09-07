# Jira Ticket Impact Assessment for RBI

This report assesses the technical and business implications of the provided Jira tickets on the RBI (Remote Browser Isolation) system.

---

## Ticket: RBI-39226 - [ODI] Provider. Copy URL in Context menu (French Canadian)

**Description:** This ticket aims to add a "Copy URL" option to the context menu within the On-Demand Isolation (ODI) provider, specifically for French Canadian localization. This functionality allows users to copy the currently browsed URL, which is typically embedded in the `eurl` parameter.

**Affected Components:**
*   **Provider UI/Frontend:** The context menu implementation will need to be extended to include this new option.
*   **Localization/Internationalization (i18n) Module:** Changes will be required in the resource files or code responsible for managing French Canadian translations and UI elements. Specifically, `rbi-common/src/rlocale-manager.h` and `rbi-common/src/rlocale-manager.cpp` are likely candidates for handling locale-specific strings and behaviors. The `rbi-common/src/rtranslation.h` and `.cpp` files would also be relevant for managing translations.
*   **ODI Core Logic:** The underlying mechanism for extracting and copying the URL from the `eurl` parameter might be touched, though the primary change is UI-driven.

**Current Code References (Potential):**
*   Based on the provided file list, files related to UI rendering, locale management, and potentially URL handling within the provider would be relevant. For instance:
    *   `./src/provider/core/rbi-common/src/rlocale-manager.h`
    *   `./src/provider/core/rbi-common/src/rlocale-manager.cpp`
    *   `./src/provider/core/rbi-common/src/rtranslation.h`
    *   `./src/provider/core/rbi-common/src/user-agent.h` (potentially for user-facing elements)

**Risks, Dependencies, or Required Actions:**
*   **Risk:** Incomplete or incorrect translation for French Canadian users.
*   **Risk:** UI inconsistencies if the new menu item is not styled correctly.
*   **Action:** Ensure thorough testing of the French Canadian localization.
*   **Action:** Verify that the URL extraction logic correctly identifies the target URL, especially considering potential encoding issues within the `eurl` parameter.
*   **Dependency:** Relies on the successful implementation of the "Copy URL" functionality in the base language (as indicated by reference to RBI-38869).

**Recommendations for Implementation:**
1.  **Localization String Management:** Ensure the French Canadian string for "Copy URL" is correctly integrated into the existing localization framework.
2.  **Context Menu Integration:** Implement the new context menu item, ensuring it's only displayed when appropriate and functions as expected.
3.  **Testing:** Rigorously test the functionality with French Canadian language settings. Manual testing of the use cases outlined in the ticket is crucial, and adding automated tests where feasible (e.g., checking if the string appears in the French Canadian locale) would be beneficial.

**Business Impact:**
*   **Positive:** Enhances user experience for French Canadian users by providing consistent functionality across languages. Improves accessibility and usability for a specific user segment.

---

## Ticket: RBI-39223 - [ODI] Provider. Captive navigation implementation (2)

**Description:** This ticket focuses on implementing Captive Navigation (CN) behavior within the ODI Provider. The goal is to restrict the URL displayed in the browser's address bar to the original isolated domain (e.g., `ondemand.isolation.goskope.com`) while allowing navigation to different or same domains. This is a continuation of previous work (RBI-35163) to refine the CN implementation.

**Affected Components:**
*   **ODI Core Logic:** This is the primary area of impact. The code responsible for intercepting navigation requests, modifying them to stay within the isolation domain, and handling URL redirection will be heavily involved.
*   **Provider Networking/HTTP Handling:** Components responsible for fetching web content and managing network requests will need to be aware of and potentially adapt to the CN logic.
*   **Browser Integration/Rendering:** The mechanism by which RBI interacts with the browser to display content and handle navigation events will be modified.
*   **URL Manipulation/Encoding:** Code that processes and constructs URLs will be critical, especially for embedding the target URL within the `eurl` parameter.
*   **UI Elements:** Title and favicon handling might be affected as they should reflect the isolated domain's content.
*   **History Management:** The creation of history entries needs to correctly point to the ODI URL.

**Current Code References (Potential):**
*   The broad scope of this ticket suggests modifications across several provider components. Files within `src/provider/core/` are highly likely to be affected. Specific areas include:
    *   URL processing utilities in `rbi-common`.
    *   Networking components within `slc-core-transport`.
    *   Core ODI logic within the Provider.
    *   Potentially files related to session management.
*   The mention of `eurl` parameter and `ondemand.isolation.goskope.com` points to URL handling and proxying logic.

**Risks, Dependencies, or Required Actions:**
*   **Risk:** **Scope Creep/Incomplete Implementation:** The ticket explicitly mentions that "not all initially expected deliverables will be fully completed" and "Certain parts may need to be scoped out or postponed." This is a significant risk that needs careful management.
*   **Risk:** **Navigation Failures:** Incorrect implementation could lead to broken navigation, users being unable to access intended sites, or infinite redirect loops.
*   **Risk:** **Security Vulnerabilities:** Modifying navigation and URL handling could inadvertently introduce security loopholes, e.g., allowing users to bypass isolation or exposing sensitive information.
*   **Risk:** **Performance Degradation:** The added logic for CN could introduce latency if not optimized.
*   **Risk:** **Inconsistent User Experience:** Variations in how CN behaves across different types of links (ETO/NTO, new tab/same tab) could confuse users.
*   **Dependency:** Builds upon previous work (RBI-35163) and acknowledges limitations of the current workaround.
*   **Dependency:** Requires adherence to specific "CN Requisites" and "CN Use-cases" documents.
*   **Action:** **Strict Scope Management:** The development team must actively manage the scope, prioritizing critical use cases as per the ticket's warning. A clear definition of what is *in* and *out* of scope for this iteration is essential.
*   **Action:** **Thorough Testing:** Given the complexity and potential for incomplete implementation, comprehensive testing is paramount. This includes:
    *   Unit tests for core CN logic (configuration, restriction enforcement).
    *   Functional tests covering all specified ETO/NTO navigation scenarios (same tab, new tab).
    *   Regression testing to ensure no adverse effects on existing ODI functionality.
*   **Action:** **Code Review Focus:** Code reviews should pay close attention to URL manipulation, redirection logic, and security implications.

**Recommendations for Implementation:**
1.  **Phased Rollout/Prioritization:** If scope reduction is necessary, prioritize the core functionality for same-tab navigation, then extend to new tabs and edge cases. Document clearly what is deferred.
2.  **Direct ODI Request:** Adhere to the instruction of using "Direct ODI Request has to be sent directly to Provider" instead of relying on `Forward`. This implies direct handling within the provider's request processing pipeline.
3.  **URL Structure Adherence:** Ensure the address bar URL precisely matches the specified format (`https://ondemand.isolation.goskope.com/?eurl=<url_encoded>`).
4.  **History Entry Integrity:** Verify that history entries are correctly generated using the ODI URL format.
5.  **Testability:** Implement unit and functional tests as encouraged in the ticket to ensure the robustness of the CN implementation.

**Business Impact:**
*   **Positive:** Significantly improves the user experience of ODI by providing a more seamless and secure browsing session where users don't see external domains in the address bar. This reduces potential user confusion and enhances the perceived security of the isolation.
*   **Risk:** If implementation is rushed or incomplete, it could lead to user frustration, support overhead, and a damaged perception of the ODI feature's reliability. The note about potential scope reduction is a key concern that could impact the immediate business value delivered.

---