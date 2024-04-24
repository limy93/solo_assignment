Feature: Password Reset
  As a registered user who forgot their password
  I want to be able to reset my password
  So that I can regain access to my account

  Scenario: User requests a password reset link
    Given I am on the Login page
    When I click on the "Forgot your password?" link
    And I submit my email address for password reset
    Then I should be informed to check my email for a reset link

  Scenario: User resets their password using the reset link
    Given I have a valid reset link
    When I visit the password reset link
    And I submit a new password
    Then I should see a password reset success message