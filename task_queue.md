# Task Queue

> Status: Updated 2026-04-18

## 1. Fact-check picks "see more" page: add share button

- Status: Done
- Priority: Medium
- Source issue: UI for "Fact-check picks for you" posts: add a share button to the "see more" page?
- Goal: Users can share a fact-check pick directly from the "see more" detail/list page.
- Tasks:
  - Locate the "Fact-check picks for you" component and the corresponding "see more" page/view.
  - Check how existing public/private post share actions are implemented.
  - Add a share button using the existing share UI pattern and API behavior.
  - Verify shared fact-check pick posts appear correctly in the feed and exported data.
- Acceptance criteria:
  - A visible share action exists on each fact-check pick in the "see more" page.
  - Clicking share follows the same flow as existing share interactions.
  - No regression to the existing fact-check picks display.
- Result:
  - Added a centered "Share with Group" button below the fact-check pick detail dialog content.

## 2. Fact-check picks timestamps: assess and optionally vary timestamps

- Status: Done
- Priority: Medium
- Source issue: "Fact-check picks for you" posts all have the same timestamps. Would that be an issue? Do we need to vary the timestamps?
- Goal: Determine whether identical timestamps affect UX, ordering, or research data, then implement a consistent rule if needed.
- Tasks:
  - Identify where timestamps for fact-check pick posts are generated or displayed.
  - Check whether identical timestamps affect sorting, grouping, or export interpretation.
  - Confirm the desired behavior with the experiment owner if this is a research-design decision.
  - If needed, vary timestamps deterministically by message order, user/day, or configured schedule.
- Acceptance criteria:
  - The impact of identical timestamps is documented.
  - If changed, timestamps remain stable and reproducible for export/analysis.
  - UI ordering remains predictable.
- Result:
  - Hid fact-check pick timestamps in the detail dialog instead of changing stored timestamps.

## 3. Allow users to edit or delete uploaded posts

- Status: Deferred
- Priority: Low
- Source issue: User asked whether it is possible to edit or delete posts after upload, or consider it for future experiments.
- Goal: Evaluate and, if approved, add user-facing edit/delete controls for posts created by the current user.
- Tasks:
  - Confirm scope: user-created posts only, excluding system/fact-check/daily/poll posts unless explicitly approved.
  - Review existing backend update/delete endpoints and permission checks.
  - Add frontend controls only for eligible posts owned by the current user.
  - Add confirmation for delete and preserve audit/data-export expectations.
  - Test create, edit, delete, and export behavior.
- Acceptance criteria:
  - Users can edit/delete only their own eligible posts.
  - Deleted or edited posts are represented in a way that does not break research data analysis.
  - Unauthorized edit/delete attempts are blocked server-side.
- Result:
  - Deferred by request.

## 4. Preserve unfinished share comments when the share dialog is dismissed

- Status: Done
- Priority: High
- Source issue: While typing a comment when sharing fact-check pick messages, save the unfinished comment when accidentally clicking outside the box and return to the home page.
- Goal: Prevent users from losing draft comments when the share comment box/dialog is accidentally dismissed.
- Tasks:
  - Reproduce the behavior when sharing a fact-check pick and clicking outside the comment box.
  - Identify whether the modal/dialog closes and navigates home intentionally or due to event propagation.
  - Store draft comment text per post/share context before dismissal.
  - Restore the draft when the user reopens the share flow.
  - Consider preventing accidental outside-click dismissal if that better matches the UX.
- Acceptance criteria:
  - Draft text is not lost after accidental outside click or return to home.
  - Reopening the same share flow restores the unfinished comment.
  - Successfully submitting or cancelling intentionally clears the draft.
- Result:
  - Disabled closing the share dialog by clicking outside the dialog or pressing Escape. Users can still close it with the X button.

## 5. Fix missing cover photo for Day 8 fact-check message

- Status: Ignored
- Priority: High
- Source issue: Day 8: One fact check message cover photo "COVID-19 vaccinations are safe for children" did not display.
- Goal: Ensure the Day 8 fact-check message cover image is imported, stored, and rendered correctly.
- Tasks:
  - Locate the Day 8 fact-check seed/import data and the image reference for "COVID-19 vaccinations are safe for children".
  - Check whether the image file exists in the expected static path or upload location.
  - Verify backend response includes the expected image URL.
  - Fix incorrect path, missing import, filename mismatch, or frontend rendering logic.
  - Add a regression check for missing fact-check cover images if practical.
- Acceptance criteria:
  - The target Day 8 cover photo displays in the UI.
  - The image URL works directly in the browser.
  - Other fact-check message cover photos still display.
- Result:
  - Ignored by request.

## 6. Investigate low post-survey response rate and nudge flow

- Status: Ignored
- Priority: Medium
- Source issue: Low post-survey response rate: only 1 finished after the experiment ended and another 3 completed after sending the nudge email.
- Goal: Determine whether the low response rate was caused by product/email issues or participant behavior.
- Tasks:
  - Verify post-survey email scheduling, send logs, recipient list, and delivery status.
  - Check whether survey links were generated correctly and remained accessible after experiment end.
  - Review nudge email timing and content.
  - Compare completed responses against users who received emails.
  - Document findings and recommended follow-up.
- Acceptance criteria:
  - Delivery and link-access status are known.
  - Any technical failure is identified with impacted users.
  - If no technical issue is found, document the response-rate data for research follow-up.
- Result:
  - Ignored by request.

## 7. Fix missing data in exported `tb_post_factcheck`

- Status: Ignored
- Priority: High
- Source issue: No data in the `tb_post_factcheck` export file.
- Goal: Ensure fact-check post data is included in exports.
- Tasks:
  - Reproduce the export and confirm `tb_post_factcheck` is empty.
  - Check the export implementation for `tb_post_factcheck`.
  - Verify source database table/model contains fact-check data.
  - Fix query, table name, serializer, export routing, or permission issue.
  - Re-run export and compare row counts with database counts.
- Acceptance criteria:
  - `tb_post_factcheck` export contains expected rows.
  - Exported columns match the documented/exported schema.
  - Row count is validated against the database.
- Result:
  - Ignored by request.

## 8. Document export fields `timeline_type` and `post_shared_id`

- Status: Ignored
- Priority: Medium
- Source issue: What do `timeline_type` and `post_shared_id` in the `tb_post_public` file mean?
- Goal: Provide clear definitions for these exported fields.
- Tasks:
  - Locate model definitions and export code for `tb_post_public`.
  - Trace how `timeline_type` is assigned.
  - Trace how `post_shared_id` is assigned and how it relates original/shared posts.
  - Add or update export documentation.
- Acceptance criteria:
  - `timeline_type` has a clear meaning and allowed values.
  - `post_shared_id` relationship is documented with examples.
  - Documentation matches the actual database/export behavior.
- Result:
  - Ignored by request.

## 9. Investigate comment export rows referencing missing public posts

- Status: Ignored
- Priority: High
- Source issue: In the comment file, some main posts are missing from the public post file. Example: comment rows reference `post_id` 2707, 2709, and 2708, but those posts are not in the public post file.
- Goal: Resolve referential inconsistency between comment exports and public post exports.
- Tasks:
  - Reproduce the export and identify all comment rows whose `post_id` is missing from `tb_post_public`.
  - Check whether missing posts are private, deleted, fact-check, system, or another post type.
  - Determine whether comments should join to a different post export file or whether public export is incomplete.
  - Fix export logic or document cross-file relationships as appropriate.
  - Validate there are no unexpected orphan comment references after the fix.
- Acceptance criteria:
  - Every exported comment `post_id` can be resolved to a documented exported post source.
  - Public post export includes all expected public posts.
  - Known non-public references are documented clearly if they are valid.
- Result:
  - Ignored by request.
