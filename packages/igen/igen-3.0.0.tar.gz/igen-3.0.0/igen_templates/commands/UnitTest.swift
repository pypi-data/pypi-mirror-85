final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private var disposeBag: DisposeBag!

    // Triggers
{% for p in input_properties %}
    private let {{ p.name }}Trigger = PublishSubject<{{ p.type_name }}>()
{% endfor %}

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)
        
        input = {{ name }}ViewModel.Input(
        {% for p in input_properties %}
            {{ p.name }}: {{ p.name }}.asDriverOnErrorJustComplete(){{ "," if not loop.last }}
        {% endfor %}
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }
    
{% for p in input_properties %}
    func test_{{ p.name }}Trigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

{% endfor %}
}