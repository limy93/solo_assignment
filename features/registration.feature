Feature: User Registration
  As a new visitor to the website
  I want to be able to register an account
  So that I can perform actions that require authentication

  Scenario: Registering a new user
    Given I am on the Registration page
    When I enter valid registration details
    And I submit the registration form
    Then I should be registered and redirected to the Dashboard page