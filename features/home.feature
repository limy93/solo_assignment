Feature: Home Page Accessibility
  As a visitor
  I want to visit the Home page
  So that I can confirm the web application is accessible

  Scenario: The Home page loads correctly
    Given I am on the Home page
    Then I should see the page title "Welcome to EpochCraft"

  Scenario: Navigation to the Products page
    Given I am on the Home page
    When I click on the "Browse EcoCredits" button
    Then I should be redirected to the Products page

  Scenario: Navigation to the About page
    Given I am on the Home page
    When I click on the "Learn More" button
    Then I should be redirected to the About page

  Scenario: Navigation to the Impact page
    Given I am on the Home page
    When I click on the "View Details" button
    Then I should be redirected to the Impact page

  Scenario: Navigation to the Register page
    Given I am on the Home page
    When I click on the "Register Now" button
    Then I should be redirected to the Register page