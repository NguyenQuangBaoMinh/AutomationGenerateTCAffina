"""
ChatGPT Service
Call OpenAI API to generate test cases from BRD content
Focus on UI/UX testing with 3-batch strategy for 90 test cases
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatGPTService:
    """Service to interact with OpenAI ChatGPT API"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize ChatGPT service

        Args:
            api_key: OpenAI API key (if None, loads from environment)
            model: Model to use (if None, loads from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')

        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file")

        self.client = OpenAI(api_key=self.api_key)

    def _create_prompt_ui_happy_path(self, brd_content: str, count: int = 30) -> str:
        """
        Create prompt for generating UI Happy Path test cases

        Args:
            brd_content: BRD document content
            count: Number of test cases to generate

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert QA UI/UX Test Engineer for an insurance company.

Analyze the following BRD (Business Requirements Document) and generate EXACTLY {count} test cases focusing on UI/UX HAPPY PATH scenarios.

BRD CONTENT:
{brd_content}

FOCUS AREAS FOR THIS BATCH:
1. Main user flows working correctly (navigation, form submission)
2. UI elements displaying properly (buttons, fields, labels, images)
3. Successful scenarios (user completes tasks without errors)
4. Page transitions and navigation between screens
5. Data display and presentation on UI

TEST CASE REQUIREMENTS:
- Focus ONLY on UI/UX testing (NOT backend/API/database)
- Test user interface elements: buttons, forms, fields, dropdowns, checkboxes, etc.
- Test visual elements: layout, alignment, colors, fonts, spacing
- Test user interactions: click, type, select, navigate
- Describe WHAT USER SEES and WHAT USER DOES on the UI
- Each test case MUST include:
  * description: Clear UI-focused description
  * steps: Detailed UI interaction steps (use \\n for line breaks)
  * expected_result: What user sees on screen (UI feedback)
  * priority: "High" for critical UI flows, "Medium" for secondary

OUTPUT FORMAT - MUST be valid JSON array ONLY:
[
  {{
    "description": "Verify health insurance selection button displays and is clickable",
    "steps": "1. Open the insurance selection page\\n2. Locate the 'Health Insurance' button\\n3. Verify button is visible and enabled\\n4. Click on the button",
    "expected_result": "Button changes color on hover, page navigates to health insurance form, form fields are displayed correctly",
    "priority": "High"
  }},
  ...
]

IMPORTANT:
- Output ONLY the JSON array, no markdown, no explanations
- Generate EXACTLY {count} test cases
- Use Vietnamese if BRD is in Vietnamese
- Focus on UI elements, user interactions, visual verification
- NO technical/backend testing (no API, database, server tests)
"""
        return prompt

    def _create_prompt_ui_validation(self, brd_content: str, count: int = 30) -> str:
        """
        Create prompt for generating UI Validation & Interaction test cases

        Args:
            brd_content: BRD document content
            count: Number of test cases to generate

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert QA UI/UX Test Engineer for an insurance company.

Analyze the following BRD (Business Requirements Document) and generate EXACTLY {count} test cases focusing on UI VALIDATION & USER INTERACTIONS.

BRD CONTENT:
{brd_content}

FOCUS AREAS FOR THIS BATCH:
1. Form field validation (required fields, format validation, length limits)
2. Input field behaviors (placeholder text, error messages, success indicators)
3. Button states (enabled/disabled/loading states)
4. Dropdown/select behaviors (options display, selection feedback)
5. Checkbox/radio button interactions
6. Error message display and formatting
7. Tooltip and help text display
8. User input feedback (typing indicators, character counters)

TEST CASE REQUIREMENTS:
- Focus on UI VALIDATION and USER INTERACTION feedback
- Test what happens when user enters invalid/valid data
- Test UI response to user actions
- Verify error messages, validation messages display correctly on UI
- Test field-level interactions (focus, blur, typing, selecting)
- Each test case MUST include:
  * description: Clear UI validation scenario
  * steps: Detailed interaction steps on UI
  * expected_result: UI feedback user sees (error messages, visual indicators)
  * priority: "Medium" for most validation tests

OUTPUT FORMAT - MUST be valid JSON array ONLY:
[
  {{
    "description": "Verify error message displays when required field is left empty",
    "steps": "1. Open insurance application form\\n2. Leave 'Full Name' field empty\\n3. Click Submit button\\n4. Observe error message",
    "expected_result": "Red error message appears below field stating 'Full Name is required', field border turns red, submit button remains enabled",
    "priority": "Medium"
  }},
  ...
]

IMPORTANT:
- Output ONLY the JSON array, no markdown, no explanations
- Generate EXACTLY {count} test cases
- Use Vietnamese if BRD is in Vietnamese
- Focus on UI validation feedback, not backend validation
- Test visual feedback user sees on screen
"""
        return prompt

    def _create_prompt_ui_edge_cases(self, brd_content: str, count: int = 30) -> str:
        """
        Create prompt for generating UI Edge Cases & Responsive test cases

        Args:
            brd_content: BRD document content
            count: Number of test cases to generate

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert QA UI/UX Test Engineer for an insurance company.

Analyze the following BRD (Business Requirements Document) and generate EXACTLY {count} test cases focusing on UI EDGE CASES, RESPONSIVE DESIGN, and CROSS-BROWSER testing.

BRD CONTENT:
{brd_content}

FOCUS AREAS FOR THIS BATCH:
1. Boundary testing (max length inputs, special characters, very long text)
2. Responsive design (mobile, tablet, desktop views)
3. Browser compatibility (Chrome, Safari, Firefox, Edge)
4. UI edge cases (window resize, zoom in/out, orientation change)
5. Accessibility (keyboard navigation, tab order, screen reader support)
6. Visual regression (layout breaks, overlapping elements, cut-off text)
7. Empty states and loading states
8. Performance UI feedback (slow loading, large data sets)

TEST CASE REQUIREMENTS:
- Focus on EDGE CASES and CROSS-DEVICE testing
- Test UI behavior in unusual but valid scenarios
- Test responsive design across different screen sizes
- Test accessibility features
- Verify UI doesn't break under edge conditions
- Each test case MUST include:
  * description: Clear edge case or responsive scenario
  * steps: Detailed steps including device/browser context
  * expected_result: UI behavior and layout expectations
  * priority: "Medium" or "Low" based on criticality

OUTPUT FORMAT - MUST be valid JSON array ONLY:
[
  {{
    "description": "Verify form layout remains intact when browser window is resized to tablet width (768px)",
    "steps": "1. Open insurance form on desktop browser\\n2. Resize browser window to 768px width\\n3. Observe form layout and field alignment\\n4. Try filling and submitting form",
    "expected_result": "Form fields stack vertically, buttons remain visible and clickable, no horizontal scrolling, all text remains readable, no overlapping elements",
    "priority": "Medium"
  }},
  ...
]

IMPORTANT:
- Output ONLY the JSON array, no markdown, no explanations
- Generate EXACTLY {count} test cases
- Use Vietnamese if BRD is in Vietnamese
- Focus on UI edge cases, responsive behavior, visual consistency
- Test cross-device and cross-browser UI rendering
"""
        return prompt

    def _call_chatgpt(self, prompt: str, max_tokens: int = 4000) -> Tuple[bool, str, Optional[str]]:
        """
        Call ChatGPT API

        Args:
            prompt: Prompt to send
            max_tokens: Maximum tokens in response

        Returns:
            Tuple of (success, response_text, error_message)
        """
        try:
            print(f"🤖 Calling ChatGPT API ({self.model})...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert QA UI/UX Test Engineer specializing in generating comprehensive UI/UX test cases. Always output valid JSON only. Focus on user interface testing, not backend or technical testing."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7  # Balanced creativity and consistency
            )

            response_text = response.choices[0].message.content

            # Log token usage
            print(f"✓ API call successful")
            print(f"  - Input tokens: {response.usage.prompt_tokens}")
            print(f"  - Output tokens: {response.usage.completion_tokens}")
            print(f"  - Total tokens: {response.usage.total_tokens}")

            return True, response_text, None

        except Exception as e:
            error_msg = f"ChatGPT API error: {str(e)}"
            print(f"✗ {error_msg}")
            return False, "", error_msg

    def _parse_test_cases(self, response_text: str) -> Tuple[bool, List[Dict], Optional[str]]:
        """
        Parse test cases from ChatGPT response

        Args:
            response_text: Raw response from ChatGPT

        Returns:
            Tuple of (success, test_cases_list, error_message)
        """
        try:
            # Remove markdown code blocks if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```'):
                # Remove ```json or ``` at start
                cleaned_text = cleaned_text.split('\n', 1)[1] if '\n' in cleaned_text else cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text.rsplit('```', 1)[0]

            cleaned_text = cleaned_text.strip()

            # Parse JSON
            test_cases = json.loads(cleaned_text)

            # Validate it's a list
            if not isinstance(test_cases, list):
                return False, [], "Response is not a JSON array"

            # Validate each test case has required fields
            required_fields = ['description', 'steps', 'expected_result', 'priority']
            for i, tc in enumerate(test_cases):
                for field in required_fields:
                    if field not in tc:
                        return False, [], f"Test case {i+1} missing required field: {field}"

            print(f"✓ Successfully parsed {len(test_cases)} test cases")
            return True, test_cases, None

        except json.JSONDecodeError as e:
            return False, [], f"Failed to parse JSON: {str(e)}"
        except Exception as e:
            return False, [], f"Parsing error: {str(e)}"

    def generate_test_cases(
        self,
        brd_content: str,
        target_count: int = 90,
        batch_mode: bool = True
    ) -> Tuple[bool, List[Dict], Optional[str]]:
        """
        Generate UI/UX test cases from BRD content using 3-batch strategy

        Args:
            brd_content: BRD document text content
            target_count: Target number of test cases (default: 90, recommended: 70-90)
            batch_mode: If True, generates in 3 batches (UI Happy + Validation + Edge Cases)

        Returns:
            Tuple of (success, test_cases_list, error_message)
        """
        all_test_cases = []

        if batch_mode and target_count >= 70:
            # 3-BATCH STRATEGY for 70-90 test cases
            batch1_count = 30  # UI Happy Path
            batch2_count = 30  # UI Validation & Interactions
            batch3_count = target_count - 60  # UI Edge Cases & Responsive (30 if target=90)

            print(f"\n{'='*70}")
            print(f"UI/UX TEST GENERATION STRATEGY - {target_count} test cases")
            print(f"{'='*70}")
            print(f"  Batch 1: {batch1_count} UI Happy Path test cases")
            print(f"  Batch 2: {batch2_count} UI Validation & Interaction test cases")
            print(f"  Batch 3: {batch3_count} UI Edge Cases & Responsive test cases")
            print(f"{'='*70}\n")

            # ========== BATCH 1: UI Happy Path ==========
            print(f"\n{'='*70}")
            print(f"BATCH 1: Generating {batch1_count} UI HAPPY PATH test cases")
            print(f"{'='*70}")

            prompt1 = self._create_prompt_ui_happy_path(brd_content, batch1_count)
            success1, response1, error1 = self._call_chatgpt(prompt1)

            if not success1:
                return False, [], error1

            success_parse1, happy_cases, parse_error1 = self._parse_test_cases(response1)
            if not success_parse1:
                return False, [], parse_error1

            all_test_cases.extend(happy_cases)
            print(f"✓ Batch 1 completed: {len(happy_cases)} test cases")

            # ========== BATCH 2: UI Validation & Interactions ==========
            print(f"\n{'='*70}")
            print(f"BATCH 2: Generating {batch2_count} UI VALIDATION test cases")
            print(f"{'='*70}")

            prompt2 = self._create_prompt_ui_validation(brd_content, batch2_count)
            success2, response2, error2 = self._call_chatgpt(prompt2)

            if not success2:
                # If second batch fails, return first batch only
                print(f"Batch 2 failed, returning {len(all_test_cases)} test cases from Batch 1")
                return True, all_test_cases, "Batch 2 failed but Batch 1 succeeded"

            success_parse2, validation_cases, parse_error2 = self._parse_test_cases(response2)
            if not success_parse2:
                print(f"Batch 2 parsing failed, returning {len(all_test_cases)} test cases from Batch 1")
                return True, all_test_cases, "Batch 2 parsing failed but Batch 1 succeeded"

            all_test_cases.extend(validation_cases)
            print(f"✓ Batch 2 completed: {len(validation_cases)} test cases")

            # ========== BATCH 3: UI Edge Cases & Responsive ==========
            print(f"\n{'='*70}")
            print(f"BATCH 3: Generating {batch3_count} UI EDGE CASES & RESPONSIVE test cases")
            print(f"{'='*70}")

            prompt3 = self._create_prompt_ui_edge_cases(brd_content, batch3_count)
            success3, response3, error3 = self._call_chatgpt(prompt3, max_tokens=4000)

            if not success3:
                # If third batch fails, return first two batches
                print(f"Batch 3 failed, returning {len(all_test_cases)} test cases from Batch 1+2")
                return True, all_test_cases, "Batch 3 failed but Batch 1+2 succeeded"

            success_parse3, edge_cases, parse_error3 = self._parse_test_cases(response3)
            if not success_parse3:
                print(f"Batch 3 parsing failed, returning {len(all_test_cases)} test cases from Batch 1+2")
                return True, all_test_cases, "Batch 3 parsing failed but Batch 1+2 succeeded"

            all_test_cases.extend(edge_cases)
            print(f"✓ Batch 3 completed: {len(edge_cases)} test cases")

        else:
            # Single batch mode (for targets < 70)
            print(f"\n{'='*70}")
            print(f"Generating {target_count} test cases (single batch mode)")
            print(f"{'='*70}")

            prompt = self._create_prompt_ui_happy_path(brd_content, target_count)
            success, response, error = self._call_chatgpt(prompt, max_tokens=4000)

            if not success:
                return False, [], error

            success_parse, test_cases, parse_error = self._parse_test_cases(response)
            if not success_parse:
                return False, [], parse_error

            all_test_cases = test_cases

        print(f"\n{'='*70}")
        print(f"TOTAL GENERATED: {len(all_test_cases)} UI/UX test cases")
        print(f"{'='*70}\n")

        return True, all_test_cases, None


# Convenience function
def generate_testcases_from_brd(brd_content: str, target_count: int = 90) -> Tuple[bool, List[Dict], Optional[str]]:
    """
    Quick function to generate UI/UX test cases from BRD

    Args:
        brd_content: BRD text content
        target_count: Target number of test cases (recommended: 70-90)

    Returns:
        Tuple of (success, test_cases_list, error_message)
    """
    service = ChatGPTService()
    return service.generate_test_cases(brd_content, target_count)